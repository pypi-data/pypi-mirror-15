import copy as cp
from copy import deepcopy
import csv
import pandas as pd

from ..helpers.google import get_google_csv
from ..helpers.directory import check_file_age
from ..helpers.regexes import *
from ..helpers.blanks import *


class Convert(object):
    """
    LiPD to TIME SERIES
    TIME SERIES to LiPD
    """

    def __init__(self):

        # LiPD to TS (One file at a time)
        self.ts_root = {}  # Root metadata for current LiPD.
        self.ts_chron = {}  # Chron data if available
        self.ts_tsos = {}  # Individual columns. One entry represents one TSO (to be created later)

        # TS to LiPD (Batch Process)
        self.lipd_tsos = []  # One entry for each TSO metadata dictionary
        self.lipd_master = {}  # Key: LiPD name, Value: Complete metadata dictionary (when finished)
        self.lipd_curr_tso_data = {}  # Holds metadata for current TSO being processed
        self.dataset_ext = ''  # Filename.lpd. This is what the output name will be.
        self.table = ''
        self.variableName = ''

        # TS Names validation
        self.full_list = {"root": [], "pub": [], "climateInterpretation": [], "calibration": [], "geo": [],
                          "paleoData": []}
        # full_list - All valid TS Names and synonyms. { 'category' : [ ['validTSName', 'synonym'], ... ] }
        self.quick_list = []  # All valid TS Name keys
        self.recent = {}  # Recently corrected TS names, builds with each run.

    # LiPD TO TIME SERIES

    def ts_extract_main(self, d):
        """
        Main function to initiate LiPD to TSOs conversion.
        :param d: (dict) Metadata for one LiPD file
        """
        # Reset these each run
        self.ts_root = {}
        self.ts_tsos = {}

        # Build the root level data.
        # This will serve as the template for which column data will be added onto later.
        for k, v in d.items():
            if isinstance(v, str):
                self.ts_root[k] = v
            elif k == "funding":
                self.__ts_extract_funding(v)
            elif k == "geo":
                self.__ts_extract_geo(v)
            elif k == 'pub':
                self.__ts_extract_pub(v)
            elif k == 'chronData':
                self.ts_root[k] = cp.deepcopy(v)
                self.__ts_extract_chron(v)

        # Create tso dictionaries for each individual column (build on root data)
        self.__ts_extract_paleo(d)

        # Get TSNames and verify against TSOs in ts_tsos
        self.__fetch_tsnames()
        self.__verify_tsnames()

        return self.ts_tsos

    def __ts_extract_funding(self, l):
        """
        Creates flat funding dictionary.
        :param l: (list) Funding entries
        """
        for idx, i in enumerate(l):
            for k, v in i.items():
                self.ts_root['funding' + str(idx+1) + '_' + k] = v
        return

    def __ts_extract_geo(self, d):
        """
        Extract geo data from input
        :param d: (d) Geo dictionary
        """
        # May not need these if the key names are corrected in the future.
        x = ['geo_meanLat', 'geo_meanLon', 'geo_meanElev']
        # Iterate through geo dictionary
        for k, v in d.items():
            # Case 1: Coordinates special naming
            if k == 'coordinates':
                for idx, p in enumerate(v):
                    try:
                        # Check that our value is not in EMPTY.
                        if isinstance(p, str):
                            if p.lower() in EMPTY:
                                # If elevation is a string or 0, don't record it
                                if idx != 2:
                                    # If long ot lat is empty, set it as 0 instead
                                    self.ts_root[x[idx]] = 0
                            else:
                                # Set the value as a float into its entry.
                                self.ts_root[x[idx]] = float(p)
                        # Value is a normal number, or string representation of a number
                        else:
                            # Set the value as a float into its entry.
                            self.ts_root[x[idx]] = float(p)

                    except IndexError:
                        continue
            # Case 2: Any value that is a string can be added as-is
            elif isinstance(v, str):
                if k == 'meanElev':
                    try:
                        # Some data sets have meanElev listed under properties for some reason.
                        self.ts_root['geo_' + k] = float(v)
                    except ValueError:
                        # If the value is a string, then we don't want it
                        continue
                else:
                    self.ts_root['geo_' + k] = v
            # Case 3: Nested dictionary. Recursion
            elif isinstance(v, dict):
                self.__ts_extract_geo(v)

        return

    def __ts_extract_pub(self, l):
        """
        Extract publication data from one or more publication entries.
        :param l: (list) Publication list
        """
        # For each publication entry
        for idx, pub in enumerate(l):
            # Get author data first, since that's the most ambiguously structured data.
            self.__ts_extract_authors(pub, idx)

            # Go through data of this publication
            for k, v in pub.items():
                # Case 1: DOI ID. Don't need the rest of 'identifier' dict
                if k == 'identifier':
                    try:
                        self.ts_root['pub' + str(idx+1) + '_DOI'] = v[0]['id']
                    except KeyError:
                        continue
                # Case 2: All other string entries
                else:
                    if k != 'authors' and k != 'author':
                        self.ts_root['pub' + str(idx+1) + '_' + k] = v

        return

    def __ts_extract_authors(self, pub, idx):
        """
        Create a concatenated string of author names. Separate names with semi-colons.
        :param pub: (unknown type) Publication author structure is ambiguous
        :param idx: (int) Index number of Pub
        """
        try:
            # DOI Author data. We'd prefer to have this first.
            names = pub['author']
        except KeyError:
            try:
                # Manually entered author data. This is second best.
                names = pub['authors']
            except KeyError:
                # Couldn't find any author data. Skip it altogether.
                names = False

        # If there is author data, find out what type it is
        if names:
            # Build author names onto empty string
            auth = ''
            # Is it a list of dicts or a list of strings? Could be either
            # Authors: Stored as a list of dictionaries or list of strings
            if isinstance(names, list):
                for name in names:
                    if isinstance(name, str):
                        auth += name + ';'
                    elif isinstance(name, dict):
                        for k, v in name.items():
                            auth += v + ';'
            elif isinstance(names, str):
                auth = names
            # Enter finished author string into target
            self.ts_root['pub' + str(idx+1) + '_author'] = auth[:-1]
        return

    def __ts_extract_chron(self, d):
        """
        Extract chron data and values and make a pandas Series object. Add to ts_root
        :param dict d: Metadata dictionary
        :return dict:
        """
        # TODO make a pandas data frame out of the chron variables and values.
        s = {}
        try:
            for table_name, table_data in d.items():
                for col, col_data in table_data["columns"].items():
                    s[col] = pd.Series(col_data["values"])
        except KeyError:
            pass

        self.ts_root['chronData_df'] = pd.DataFrame(s)
        return

    def __ts_extract_paleo(self, d):
        """
        Extract all data from a PaleoData dictionary.
        :param d: (dict) PaleoData dictionary
        """
        try:
            # For each table in paleoData
            for k, v in d['paleoData'].items():
                # Get root items for this table
                self.__ts_extract_paleo_table_root(v)
                # Add age, depth, and year columns to ts_root if available
                self.__ts_extract_special(v)

                # Start creating TSOs with dictionary copies.
                for i, e in v['columns'].items():
                    if not any(x in i for x in ('age', 'depth', 'year')):
                        # TSO. Add this column onto root items. Deepcopy since we need to reuse ts_root
                        col = self.__ts_extract_paleo_columns(e, deepcopy(self.ts_root))
                        try:
                            self.ts_tsos[d['dataSetName'] + '_' + k + '_' + i] = col
                        except KeyError:
                            self.ts_tsos['dataset' + '_' + k + '_' + i] = col

        except KeyError:
            pass
        return

    def __ts_extract_special(self, d):
        """
        Extract year, age, and depth column. Add to self.ts_root
        :param dict d: Column data
        :return:
        """
        # Add age, year, and depth columns to ts_root where possible
        for i, e in d['columns'].items():
            if any(x in i for x in ('age', 'depth', 'year')):
                # Some keys have units hanging on them (i.e. 'year_ad', 'depth_cm'). We don't want units on the keys
                if re_pandas_x_und.match(i):
                    s = i.split('_')[0]
                else:
                    s = i
                if s:
                    try:
                        self.ts_root[s] = e['values']
                        self.ts_root[s + 'Units'] = e['units']
                    except KeyError:
                        # Values key was not found.
                        pass
        return

    def __ts_extract_paleo_table_root(self, d):
        """
        Extract data from the root level of a paleoData table.
        :param d: (dict) One paleoData table
        """
        for k, v in d.items():
            if isinstance(v, str):
                self.ts_root['paleoData_' + k] = v
        return

    def __ts_extract_paleo_columns(self, d, tmp_tso):
        """
        Extract data from one paleoData column
        :param d: (dict) Column dictionary
        :param tmp_tso: (dict) TSO dictionary with only root items
        :return: (dict) Finished TSO
        """
        for k, v in d.items():
            if k == 'climateInterpretation':
                tmp_tso = self.__ts_extract_climate(v, tmp_tso)
            elif k == 'calibration':
                tmp_tso = self.__ts_extract_calibration(v, tmp_tso)
            else:
                # Assume if it's not a special nested case, then it's a string value
                tmp_tso['paleoData_' + k] = v
        return tmp_tso

    @staticmethod
    def __ts_extract_calibration(d, tmp_tso):
        """
        Get calibration info from column data.
        :param d: (dict) Calibration dictionary
        :param tmp_tso: (dict) Temp TSO dictionary
        :return: (dict) tmp_tso with added calibration entries
        """
        for k, v in d.items():
            tmp_tso['calibration_' + k] = v
        return tmp_tso

    @staticmethod
    def __ts_extract_climate(d, tmp_tso):
        """
        Get climate interpretation from column data.
        :param d: (dict) Climate Interpretation dictionary
        :param tmp_tso: (dict) Temp TSO dictionary
        :return: (dict) tmp_tso with added climateInterpretation entries
        """
        for k, v in d.items():
            tmp_tso['climateInterpretation_' + k] = v
        return tmp_tso

    # TIME SERIES to LiPD

    def lipd_extract_main(self, lipd_tsos):
        """
        Main function to initiate TimeSeries to LiPD conversion
        :param lipd_tsos: (list of dict) List of all TSOs
        :return:
        """
        # Reset for each run
        self.lipd_tsos = lipd_tsos  # All TSO metadata dictionaries
        self.lipd_master = {}  # All lipds (in progress) by dataset name. Key: LiPD name, Val: JSON metadata
        self.lipd_curr_tso_data = {}  # Current TSO metadata

        # Receive list of TSO objects
        for tso in self.lipd_tsos:
            # Set current keys
            self.dataset_ext = tso['name']
            self.lipd_curr_tso_data = tso['data']
            self.__lipd_set_current()

            # Since root items are the same in the same dataset, we only need these steps if dataset doesn't exist yet.
            if self.dataset_ext not in self.lipd_master:
                self.__lipd_extract_roots()

            # Extract PaleoData, Calibration, and Climate Interpretation
            self.__lipd_extract_paleo()

        return self.lipd_master

    def __lipd_set_current(self):
        """
        Set keys for current TSO file
        """
        # Get key info
        try:
            self.table = self.lipd_curr_tso_data['paleoData_paleoDataTableName']
            self.variableName = self.lipd_curr_tso_data['paleoData_variableName']
        except KeyError:
            print("KeyError: Initial keys")
        return

    def __lipd_extract_roots(self):
        """
        Extract root from TimeSeries
        """
        tmp_funding = {}
        tmp_pub = {}
        tmp_master = {'pub': [], 'geo': {'geometry': {'coordinates': []}, 'properties': {}}, 'funding': [],
                      'paleoData': {}}
        p_keys = ['siteName', 'pages2kRegion']
        c_keys = ['meanLat', 'meanLon', 'meanElev']
        c_vals = [0, 0, 0]

        for k, v in self.lipd_curr_tso_data.items():
            if 'paleoData' not in k and 'calibration' not in k and 'climateInterpretation' not in k:
                if 'funding' in k:
                    # Group funding items in tmp_funding by number
                    m = re_fund_valid.match(k)
                    try:
                        tmp_funding[m.group(1)][m.group(2)] = v
                    except KeyError:
                        tmp_funding[m.group(1)] = {}
                        tmp_funding[m.group(1)][m.group(2)] = v

                elif 'geo' in k:
                    key = k.split('_')
                    # Coordinates
                    if key[1] in c_keys:
                        if key[1] == 'meanLat':
                            c_vals[0] = v
                        elif key[1] == 'meanLon':
                            c_vals[1] = v
                        elif key[1] == 'meanElev':
                            c_vals[2] = v
                    # Properties
                    elif key[1] in p_keys:
                        tmp_master['geo']['properties'][key[1]] = v
                    # All others
                    else:
                        tmp_master['geo'][key[1]] = v

                elif 'pub' in k:
                    # Group pub items in tmp_pub by number
                    m = re_pub_valid.match(k)
                    number = int(m.group(1)) - 1  # 0 indexed behind the scenes, 1 indexed to user.
                    key = m.group(2)
                    # Authors ("Pu, Y.; Nace, T.; etc..")
                    if key == 'author' or key == 'authors':
                        try:
                            tmp_pub[number]['author'] = self.__lipd_extract_author(v)
                        except KeyError:
                            tmp_pub[number] = {}
                            tmp_pub[number]['author'] = self.__lipd_extract_author(v)
                    # DOI ID
                    elif key == 'DOI':
                        try:
                            tmp_pub[number]['identifier'] = [{"id": v, "type": "doi", "url": "http://dx.doi.org/" + str(v)}]
                        except KeyError:
                            tmp_pub[number] = {}
                            tmp_pub[number]['identifier'] = [{"id": v, "type": "doi", "url": "http://dx.doi.org/" + str(v)}]
                    # All others
                    else:
                        try:
                            tmp_pub[number][key] = v
                        except KeyError:
                            tmp_pub[number] = {}
                            tmp_pub[number][key] = v
                else:
                    # Root
                    tmp_master[k] = v

        # Append pub and funding to master
        for k, v in tmp_pub.items():
            tmp_master['pub'].append(v)
        for k, v in tmp_funding.items():
            tmp_master['funding'].append(v)
        # Get rid of elevation coordinate if one was never added.
        if c_vals[2] == 0:
            del c_vals[2]
        tmp_master['geo']['geometry']['coordinates'] = c_vals

        # If we're getting root info, then there shouldn't be a dataset entry yet.
        # Create entry in object master, and set our new data to it.
        self.lipd_master[self.dataset_ext] = {}
        self.lipd_master[self.dataset_ext] = tmp_master

        return

    @staticmethod
    def __lipd_extract_author(s):
        """
        Split author string back into organized dictionary
        :param s: (str) Formatted names string "Last, F.; Last, F.; etc.."
        :return: (list of dictionaries) One dictionary per author name
        """
        l = []
        authors = s.split(';')
        for author in authors:
            l.append({'name': author})
        return l

    def __lipd_extract_paleo_root(self):
        """
        Create paleo table in master if it doesn't exist. Insert table root items
        """

        try:
            # If table doesn't exist yet, create it.
            if self.table not in self.lipd_master[self.dataset_ext]['paleoData']:
                t_root_keys = ['filename', 'googleWorkSheetKey', 'paleoDataTableName']
                self.lipd_master[self.dataset_ext]['paleoData'][self.table] = {'columns': {}}
                for key in t_root_keys:
                    try:
                        # Now set the root table items in our new table
                        self.lipd_master[self.dataset_ext]['paleoData'][self.table][key] = self.lipd_curr_tso_data['paleoData_' + key]
                    except KeyError:
                        # That's okay. Keep trying :)
                        continue
        except KeyError:
            print("KeyError lipd_extract_paleo: Inserting table ")

        return

    def __lipd_extract_paleo(self):
        """
        Extract paleoData from tso
        :return: LiPD entry in self.lipd_master is updated
        """
        tmp_clim = {}
        tmp_cal = {}

        self.__lipd_extract_paleo_root()

        try:
            # Create the column entry in the table
            self.lipd_master[self.dataset_ext]['paleoData'][self.table]['columns'][self.variableName] = {}
            # Start inserting paleoData into the table at self.lipd_master[table][column]
            for k, v in self.lipd_curr_tso_data.items():
                # ['paleoData', 'key']
                m = k.split('_')
                if 'paleoData' in m[0]:
                    self.lipd_master[self.dataset_ext]['paleoData'][self.table]['columns'][self.variableName][m[1]] = v
                elif 'calibration' in m[0]:
                    tmp_cal[m[1]] = v
                elif 'climateInterpretation' in m[0]:
                    tmp_clim[m[1]] = v

        except KeyError:
            print("KeyError lipd_extract_paleo: Inserting column data ")

        # If these sections had any items added to them, then add them to the column master.
        if tmp_clim:
            self.lipd_master[self.dataset_ext]['paleoData'][self.table]['columns'][self.variableName]['climateInterpretation'] = tmp_clim
        if tmp_cal:
            self.lipd_master[self.dataset_ext]['paleoData'][self.table]['columns'][self.variableName]['calibration'] = tmp_cal
        return

    # VALIDATING AND UPDATING TSNAMES

    def __fetch_tsnames(self):
        """
        Call down a current version of the TSNames spreadsheet from google. Convert to a structure better
        for comparisons.
        :return: (self.full_list) Keys: Valid TSName, Values: TSName synonyms
        :return: (self.quick_list) List of valid TSnames
        """

        # Check if it's been longer than one day since updating the TSNames.csv file.
        # If so, go fetch the file from google in case it's been updated since.
        # Or if file isn't found at all, download it also.
        if check_file_age('tsnames.csv', 1):
            # Fetch TSNames sheet from google
            print("Fetching update for TSNames.csv")
            ts_id = '1C135kP-SRRGO331v9d8fqJfa3ydmkG2QQ5tiXEHj5us'
            get_google_csv(ts_id, 'tsnames.csv')
        try:
            # Start sorting the tsnames into an organized structure
            with open('tsnames.csv', 'r') as f:
                r = csv.reader(f, delimiter=',')
                for idx, line in enumerate(r):
                    # print('line[{}] = {}'.format(i, line))
                    if idx != 0:
                        # Do not record empty lines. Create list of non-empty entries.
                        line = [x for x in line if x]
                        # If line has content (i.e. not an empty line), then record it
                        if line:
                            # We don't need all the duplicates of pub and fund.
                            if "pub" in line[0] or "funding" in line[0]:
                                if re_pub_fetch.match(line[0]):
                                    self.quick_list.append(line[0])
                                    self.full_list['pub'].append(line)
                            elif re_misc_fetch.match(line[0]):
                                # Other Categories. Not special
                                self.quick_list.append(line[0])
                                cat, key = line[0].split('_')
                                self.full_list[cat].append(line)
                            else:
                                # Any of the root items
                                self.quick_list.append(line[0])
                                self.full_list["root"].append(line)
        except FileNotFoundError:
            print("CSV FileNotFound: TSNames")

        return

    def __verify_tsnames(self):
        """
        Verify TSNames are current and valid. Compare to TSNames spreadsheet in Google Drive. Update where necessary.
        """
        # Temp to store incorrect keys
        bad_keys = []

        for name, tso in self.ts_tsos.items():
            # Build onto the "recent" dictionary so we have a list of keys to replace.
            for k, v in tso.items():
                # @context needs to be ignored
                if k not in self.quick_list and not re_pub_valid.match(k) and not re_fund_valid.match(k) and k != '@context':
                    # Invalid key. Store in temp for processing.
                    if k not in self.recent:
                        bad_keys.append(k)
            # Start to find replacements for empty entries in "recent"
            for incorrect in bad_keys:
                # Set incorrect name as key, and valid name as value.
                self.recent[incorrect] = self.__get_valid_tsname(incorrect)

            # Use temp to start replacing entries in d
            for invalid, valid in self.recent.items():
                try:
                    # Add new item, and remove old item in one step
                    tso[valid] = tso.pop(invalid)
                except KeyError:
                    continue

        return

    def __get_valid_tsname(self, invalid):
        """
        Turn a bad tsname into a valid one.
        * Note: Index[0] for each TSName is the most current, valid entry. Index[1:] are synonyms
        :param invalid_l: (str) Invalid tsname
        :return: (str) valid tsname
        """
        valid = ''
        invalid_l = invalid.lower()
        try:
            # PUB ENTRIES
            if re_pub_invalid.match(invalid_l):

                # Case 1: pub1_year (number and hyphen)
                if re_pub_nh.match(invalid_l):
                    s_invalid = invalid_l.split('_', 1)
                    # Check which list the key word is in
                    for line in self.full_list['pub']:
                        for key in line:
                            if s_invalid[1] in key.lower():
                                # Get the keyword from the valid entry.
                                v = line[0].split("_")
                                # Join our category with the valid keyword
                                valid = ''.join([s_invalid[0], '_', v[1]])

                # Case 2: pub_year (hyphen)
                elif re_pub_h.match(invalid_l):
                    s_invalid = invalid_l.split('_', 1)
                    # The missing pub number is the main problem, but the keyword may or may not be correct. Check.
                    for line in self.full_list['pub']:
                        for key in line:
                            if s_invalid[1] in key.lower():
                                # We're going to use the valid entry as-is, because that's what we need for this case.
                                valid = line[0]

                # Case 3: pub1year (number)
                elif re_pub_n.match(invalid_l):
                    s_invalid = re_pub_n.match(invalid_l)
                    for line in self.full_list['pub']:
                        for key in line:
                            if s_invalid.group(2) in key.lower():
                                v = line[0].split('_', 1)
                                valid = ''.join(['pub', s_invalid.group(0), v[1]])

                # Case 4: pubYear (camelcase)
                elif re_pub_cc.match(invalid_l):
                    valid = self.__iter_ts('pub', invalid_l)

            # FUNDING
            elif re_fund_invalid.match(invalid_l):
                if "grant" in invalid_l:
                    valid = 'funding1_grant'
                elif "agency" in invalid_l:
                    valid = "funding1_agency"

            # GEO
            elif re_geo_invalid.match(invalid_l):
                valid = self.__iter_ts('geo', invalid_l)

            # PALEODATA
            elif re_paleo_invalid.match(invalid_l):
                g1 = re_paleo_invalid.match(invalid_l).group(1)
                valid = self.__iter_ts('paleoData', g1)

            # CALIBRATION
            elif re_calib_invalid.match(invalid_l):
                g1 = re_calib_invalid.match(invalid_l).group(1)
                valid = self.__iter_ts('calibration', g1)

            # CLIMATE INTERPRETATION
            elif re_clim_invalid.match(invalid_l):
                g1 = re_clim_invalid.match(invalid_l).group(1)
                if 'climate' in g1:
                    g1 = re.sub('climate', '', g1)
                valid = self.__iter_ts('climateInterpretation', g1)

            else:
                # ROOT
                valid = self.__iter_ts('root', invalid_l)

            # LAST CHANCE:
            # Specific case that isn't a typical format, or no match. Go through all possible entries.
            if not valid:
                valid = self.__iter_ts(None, invalid_l)

        except IndexError:
            print("ERROR: TSName indexerror")

        if not valid:
            print("ERROR: TSName unable to find match: " + invalid)
            return invalid

        return valid

    def __iter_ts(self, category, invalid):
        """
        Match an invalid entry to one of the TSName synonyms.
        :param category: (str) Name of category being searched
        :param invalid: (str) Invalid tsname string
        :return: (str) Valid tsname
        """
        valid = ''

        # If a leading hyphen is in the string, get rid of it.
        if '_' == invalid[0]:
            invalid = invalid[1:]

        # If one specific category is passed through
        if category:
            for line in self.full_list[category]:
                for key in line:
                    if invalid in key.lower():
                        valid = line[0]
                        break
        # Entire TSNames dict is passed through (i.e. final effort, all categories have failed so far)
        else:
            for k, v in self.full_list.items():
                for line in v:
                    for key in line:
                        if invalid in key.lower():
                            valid = line[0]
                            break

        return valid

    # HELPERS

    # def create_tso(self):
    #     """
    #     Creates a TimeSeriesObject and add it to the TimeSeriesLibrary
    #     :return: (obj) Time Series Object
    #     """
    #     for name, tso in self.ts_tsos.items():
    #         TimeSeries().load(tso)
    #     return
