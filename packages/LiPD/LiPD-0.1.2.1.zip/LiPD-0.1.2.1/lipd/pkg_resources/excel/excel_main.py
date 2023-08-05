import csv
import logging

import xlrd

from ..doi.doi_resolver import *
from ..helpers.bag import *
from ..helpers.directory import *
from ..helpers.zips import *

# GLOBALS
EMPTY = ['', ' ', None, 'na', 'nan']


def excel():
    """
    Parse data from Excel spreadsheets into LiPD files.
    :return:
    """

    dir_root = os.getcwd()

    # Ask user if they want to run the Chronology sheets or flatten the JSON files.
    # This is an all or nothing choice
    # need_response = True
    # while need_response:
    #     chron_run = input("Run Chronology? (y/n)\n")
    #     if chron_run == 'y' or 'n':
    #         flat_run = input("Flatten JSON? (y/n)\n")
    #         if flat_run == 'y' or 'n':
    #             need_response = False

    # For testing, assume we don't want to run these to make things easier for now.
    chron_run = 'n'
    flat_run = 'n'

    # Compile list of excel files (both types)
    f_list = list_files('.xls') + list_files('.xlsx')
    print("Found " + str(len(f_list)) + " Excel files")

    # Run once for each file
    for name_ext in f_list:

        # Filename without extension
        name = os.path.splitext(name_ext)[0]
        name_lpd = name + '.lpd'
        print("processing: {}".format(name_ext))

        # Create a temporary folder and set paths
        dir_tmp = create_tmp_dir()
        dir_bag = os.path.join(dir_tmp, name)
        dir_data = os.path.join(dir_bag, 'data')
        # Make folders in tmp
        os.mkdir(os.path.join(dir_bag))
        os.mkdir(os.path.join(dir_data))

        data_sheets = []
        chron_sheets = []
        chron_combine = []
        data_combine = []
        finalDict = OrderedDict()

        # Open excel workbook with filename
        try:
            workbook = xlrd.open_workbook(name_ext)
            # Check what worksheets are available, so we know how to proceed.
            for sheet in workbook.sheet_names():
                if 'Metadata' in sheet:
                    metadata_str = 'Metadata'
                elif 'Chronology' in sheet:
                    chron_sheets.append(sheet)
                elif 'Data' in sheet:
                    data_sheets.append(sheet)

            # METADATA WORKSHEETS
            # Parse Metadata sheet and add to output dictionary
            if metadata_str:
                cells_down_metadata(workbook, metadata_str, 0, 0, finalDict)

            # DATA WORKSHEETS
            for sheet_str in data_sheets:
                # Parse each Data sheet. Combine into one dictionary
                sheet_str = cells_down_datasheets(name, workbook, sheet_str, 2, 0)
                data_combine.append(sheet_str)

            # Add data dictionary to output dictionary
            finalDict['paleoData'] = data_combine

            # CHRONOLOGY WORKSHEETS
            chron_dict = OrderedDict()
            if chron_run == 'y':
                for sheet_str in chron_sheets:
                    # Parse each chronology sheet. Combine into one dictionary
                    temp_sheet = workbook.sheet_by_name(sheet_str)
                    chron_dict['filename'] = str(name) + '-' + str(sheet_str) + '.csv'

                    # Create a dictionary that has a list of all the columns in the sheet
                    start_row = traverse_to_chron_var(temp_sheet)
                    columns_list_chron = get_chron_var(temp_sheet, start_row)
                    chron_dict['columns'] = columns_list_chron
                    chron_combine.append(chron_dict)

                # Add chronology dictionary to output dictionary
                finalDict['chronData'] = chron_combine

            # OUTPUT

            # Now that we have all our data (almost, need csv) switch to dir_data to create files.
            os.chdir(dir_data)

            # CSV - DATA
            for sheet_str in data_sheets:
                output_csv_datasheet(workbook, sheet_str, name)
            del data_sheets[:]

            # CSV - CHRONOLOGY
            if chron_run == 'y':
                for sheet_str in chron_sheets:
                    output_csv_chronology(workbook, sheet_str, name)

            # JSON-LD
            # Invoke DOI Resolver Class to update publisher data
            finalDict = DOIResolver(dir_root, name, finalDict).main()

            # Dump finalDict to a json file.
            with open(os.path.join(dir_data, name + '.jsonld'), 'w+') as jld_file:
                json.dump(finalDict, jld_file, indent=2, sort_keys=True)

            # JSON FLATTEN code would go here.

            # Move files to bag root for re-bagging
            # dir : dir_data -> dir_bag
            dir_cleanup(dir_bag, dir_data)

            # Create a bag for the 3 files
            new_bag = create_bag(dir_bag)
            open_bag(dir_bag)
            new_bag.save(manifests=True)

            # dir: dir_tmp -> dir_root
            os.chdir(dir_root)

            # Check if same lpd file exists. If so, delete so new one can be made
            if os.path.isfile(name_lpd):
                os.remove(name_lpd)

            # Zip dir_bag. Creates in dir_root directory
            re_zip(dir_tmp, name, name_lpd)
            os.rename(name_lpd + '.zip', name_lpd)

        except Exception as e:
            # There was a problem opening a file with XLRD
            print("exception: " + str(e) + name)
            logging.exception("main(): Error opening file. - " + name)

        # Move back to dir_root for next loop.
        os.chdir(dir_root)

        # Cleanup and remove tmp directory
        shutil.rmtree(dir_tmp)

    txt_log_end(dir_root, 'quarantine.txt')
    print("Process Complete")
    return


def output_csv_datasheet(workbook, sheet, name):
    """
    Output data columns to a csv file
    :param workbook: (obj)
    :param sheet: (str)
    :param name: (str)
    :return: (none)
    """
    temp_sheet = workbook.sheet_by_name(sheet)

    # Create CSV file and open
    file_csv = open(str(name) + '-' + str(sheet) + '.csv', 'w', newline='')
    w = csv.writer(file_csv)

    try:
        # Loop to find starting variable name
        # Try to find if there are variable headers or not
        ref_first_var = traverse_short_row_str(temp_sheet)

        # Traverse down to the "Missing Value" cell to get us near the data we want.
        missing_val_row = traverse_missing_value(temp_sheet)

        # Get the missing val for search-and-replace later
        missing_val = get_missing_val(temp_sheet)

        # Loop for 5 times past "Missing Value" to see if we get a match on the variable header
        # Don't want to loop for too long, or we're wasting our time.
        position_start = var_headers_check(temp_sheet, missing_val_row, ref_first_var)
        data_cell_start = traverse_headers_to_data(temp_sheet, position_start)

        # Loop over all variable names, and count how many there are. We need to loop this many times.
        first_short_cell = traverse_short_row_int(temp_sheet)
        var_limit = count_vars(temp_sheet, first_short_cell)

        # Until we reach the bottom worksheet
        current_row = data_cell_start
        while current_row < temp_sheet.nrows:
            data_list = []

            # Move down a row and go back to column 0
            current_column = 0

            # Until we reach the right side worksheet
            while current_column < var_limit:
                # Increment to column 0, and grab the cell content
                cell_value = replace_missing_vals(temp_sheet.cell_value(current_row, current_column), missing_val)
                data_list.append(cell_value)
                current_column += 1
            data_list = replace_missing_vals(data_list, missing_val)
            w.writerow(data_list)
            current_row += 1

    except IndexError:
        pass

    file_csv.close()
    return


def output_csv_chronology(workbook, sheet, name):
    """
    Output the data columns from chronology sheet to csv file
    :param workbook: (obj)
    :param sheet: (str)
    :param name: (str)
    :return: (none)
    """
    temp_sheet = workbook.sheet_by_name(sheet)

    # Create CSV file and open
    file_csv = open(str(name) + '-' + str(sheet) + '.csv', 'w', newline='')
    w = csv.writer(file_csv)
    try:
        total_vars = count_chron_variables(temp_sheet)
        row = traverse_to_chron_data(temp_sheet)

        while row < temp_sheet.nrows:
            data_list = get_chron_data(temp_sheet, row, total_vars)
            w.writerow(data_list)
            row += 1

    except IndexError:
        logging.exception("IndexError: output_csv_chronology()")

    file_csv.close()
    return


# GEO DATA METHODS

def geometry_linestring(lat, lon, elev):
    """
    GeoJSON Linestring. Latitude and Longitude have 2 values each.
    :param lat: (list) Latitude values
    :param lon: (list) Longitude values
    :return: (dict)
    """
    d = OrderedDict()
    coordinates = []
    temp = [None, None]

    # Point type, Matching pairs.
    if lat[0] == lat[1] and lon[0] == lon[1]:
        lat.pop()
        lon.pop()
        d = geometry_point(lat, lon, elev)

    else:
        # Creates coordinates list
        for i in lat:
            temp[0] = i
            for j in lon:
                temp[1] = j
                coordinates.append(copy.copy(temp))

        # Create geometry block
        d['type'] = 'Linestring'
        d['coordinates'] = coordinates
    return d


def geometry_point(lat, lon, elev):
    """
    GeoJSON point. Latitude and Longitude only have one value each
    :param lat: (list) Latitude values
    :param lon: (list) Longitude values
    :return: (dict)
    """
    coordinates = []
    point_dict = OrderedDict()
    for idx, val in enumerate(lat):
        coordinates.append(lat[idx])
        coordinates.append(lon[idx])
    coordinates.append(elev)
    point_dict['type'] = 'Point'
    point_dict['coordinates'] = coordinates
    return point_dict


def compile_geometry(lat, lon, elev):
    """
    Take in lists of lat and lon coordinates, and determine what geometry to create
    :param lat: (list) Latitude values
    :param lon: (list) Longitude values
    :return: (dict)
    """

    while None in lat:
        lat.remove(None)
    while None in lon:
        lon.remove(None)

    # Sort lat an lon in numerical order
    lat.sort()
    lon.sort()

    # 4 coordinate values
    if len(lat) == 2 and len(lon) == 2:
        geo_dict = geometry_linestring(lat, lon, elev)

        # # 4 coordinate values
        # if (lat[0] != lat[1]) and (lon[0] != lon[1]):
        #     geo_dict = geometry_polygon(lat, lon)
        # # 3 unique coordinates
        # else:
        #     geo_dict = geometry_multipoint(lat, lon)
        #

    # 2 coordinate values
    elif len(lat) == 1 and len(lon) == 1:
        geo_dict = geometry_point(lat, lon, elev)

    # Too many points, or no points
    else:
        geo_dict = {}
        logging.exception("Error: compile_geometry()")
        print("Compile Geometry Error")

    return geo_dict


def compile_geo(d):
    """
    Compile top-level Geography dictionary.
    :param d:
    :return:
    """
    # Should probably use some IndexError catching here.
    d2 = OrderedDict()
    d2['type'] = 'Feature'
    d2['geometry'] = compile_geometry([d['latMin'], d['latMax']], [d['lonMin'], d['lonMax']], d['elevation'])
    d2['properties'] = {'siteName': d['siteName']}
    return d2


def compile_authors(cell):
    """
    Split the string of author names into the BibJSON format.
    :param cell: (str) Data from author cell
    :return: (list of dicts) Author names
    """
    author_lst = []
    s = cell.split(';')
    for w in s:
        author_lst.append(w.lstrip())
    return author_lst


# MISC HELPER METHODS


def compile_temp(d, key, value):
    """

    :param d: (dict)
    :param key: (?)
    :param value: (?)
    :return: (dict)
    """
    if not value:
        d[key] = None
    elif len(value) == 1:
        d[key] = value[0]
    else:
        d[key] = value
    return d


def compile_fund(workbook, sheet, row, col):
    """
    Compile funding entries.
    Iter both rows at the same time. Keep adding entries until both cells are empty.
    :param workbook: (obj)
    :param sheet: (str)
    :param row: (int)
    :param col: (int)
    :return: (list of dict) l
    """
    l = []
    temp_sheet = workbook.sheet_by_name(sheet)
    while col < temp_sheet.ncols:
        col += 1
        try:
            agency = temp_sheet.cell_value(row, col)
            grant = temp_sheet.cell_value(row+1, col)
            if (agency != xlrd.empty_cell and agency not in EMPTY) or (grant != xlrd.empty_cell and grant not in EMPTY):
                if agency in EMPTY:
                    l.append({'grant': grant})
                elif grant in EMPTY:
                    l.append({'agency': agency})
                else:
                    l.append({'agency': agency, 'grant': grant})

        except IndexError:
            # logging.exception("IndexError, compile_fund()")
            pass

    return l


def single_item(arr):
    """
    NOT REALLY NECESSARY.
    Check an array to see if it is a single item or not
    :param arr: (list)
    :return: (bool)
    """
    if len(arr) == 1:
        return True
    return False


def cell_occupied(temp_sheet, row, col):
    """
    Check if there is content in this cell
    :param temp_sheet: (obj)
    :param row: (int)
    :param col: (int)
    :return: (bool)
    """
    try:
        if temp_sheet.cell_value(row, col) != ("N/A" and " " and xlrd.empty_cell and ""):
            return True
    except IndexError:
        logging.exception("IndexError: cell_occupied()")
    return False


def name_to_jsonld(title_in):
    """
    Convert formal titles to camelcase json_ld text that matches our context file
    Keep a growing list of all titles that are being used in the json_ld context
    :param title_in: (str)
    :return: (str)
    """

    title_in = title_in.lower()

    # Float check for debugging. If float gets here, usually means variables are mismatched on the data sheet
    if type(title_in) is float:
        print("name_to_jsonld type error: {0}".format(title_in))

    # Sheet names
    if title_in == 'metadata':
        title_out = 'metadata'
    elif title_in == 'chronology':
        title_out = 'chronology'
    elif title_in == 'data (qc)' or title_in == 'data(qc)':
        title_out = 'dataQC'
    elif title_in == 'data (original)' or title_in == 'data(original)':
        title_out = 'dataOriginal'
    elif title_in == 'data':
        title_out = 'data'
    elif title_in == 'proxyList':
        title_out = 'proxyList'
    elif title_in == 'about':
        title_out = 'about'

    # Metadata variables
    elif 'study title' in title_in:
        title_out = 'studyTitle'
    elif 'investigators' in title_in:
        title_out = 'investigators'

    # Pub
    elif 'authors' in title_in:
        title_out = 'author'
    elif 'publication title' == title_in:
        title_out = 'title'
    elif title_in == 'journal':
        title_out = 'journal'
    elif title_in == 'year':
        title_out = 'year'
    elif title_in == 'volume':
        title_out = 'volume'
    elif title_in == 'issue':
        title_out = 'issue'
    elif title_in == 'pages':
        title_out = 'pages'
    elif title_in == 'report number':
        title_out = 'reportNumber'
    elif title_in == 'doi':
        title_out = 'id'
    elif title_in == 'abstract':
        title_out = 'abstract'
    elif 'alternate citation' in title_in:
        title_out = 'alternateCitation'

    # Geo
    elif title_in == 'site name':
        title_out = 'siteName'
    elif 'northernmost latitude' in title_in:
        title_out = 'latMax'
    elif 'southernmost latitude' in title_in:
        title_out = 'latMin'
    elif 'easternmost longitude' in title_in:
        title_out = 'lonMax'
    elif 'westernmost longitude' in title_in:
        title_out = 'lonMin'
    elif 'elevation (m)' in title_in:
        title_out = 'elevation'
    elif 'collection_name' in title_in:
        title_out = 'collectionName'

    # Funding
    elif title_in == "funding_agency_name":
        title_out = 'agency'

    # Measurement Variables
    elif title_in == 'short_name':
        title_out = 'parameter'
    elif title_in == 'what':
        title_out = 'description'
    elif title_in == 'material':
        title_out = 'material'
    elif title_in == 'error':
        title_out = 'error'

    elif title_in == 'units':
        title_out = 'units'
    elif title_in == 'seasonality':
        title_out = 'seasonality'
    elif title_in == 'archive':
        title_out = 'archive'
    elif title_in == 'detail':
        title_out = 'detail'
    elif title_in == 'method':
        title_out = 'method'
    elif title_in == 'data_type':
        title_out = 'dataType'
    elif title_in == 'basis of climate relation':
        title_out = 'basis'

    elif title_in == 'climate_interpretation_code' or title_in == 'climate_intepretation_code':
        title_out = 'climateInterpretation'

    elif title_in == 'notes' or title_in == 'comments':
        title_out = 'notes'

    else:
        return

    return title_out


def get_data_type(temp_sheet, colListNum):
    """
    Find out what type of values are stored in a specific column in data sheet (best guess)
    :param temp_sheet: (obj)
    :param colListNum: (int)
    :return: (str)
    """
    short = traverse_short_row_str(temp_sheet)
    mv_cell = traverse_missing_value(temp_sheet)
    row = var_headers_check(temp_sheet, mv_cell, short)
    temp = temp_sheet.cell_value(row, colListNum - 1)

    # Make sure we are not getting the dataType of a "NaN" item
    while (temp == 'NaN') and (row < temp_sheet.nrows):
        row += 1

    # If we find a value before reaching the end of the column, determine the dataType
    if row < temp_sheet.nrows:
        # Determine what type the item is
        str_type = instance_str(temp_sheet.cell_value(row, colListNum - 1))

    # If the whole column is NaN's, then there is no dataType
    else:
        str_type = 'None'

    return str_type


def instance_str(cell):
    """
    Tells you what data type you have, and outputs it in string form
    :param cell: (any)
    :return: (str)
    """
    if isinstance(cell, str):
        return 'str'
    elif isinstance(cell, int):
        return 'int'
    elif isinstance(cell, float):
        return 'float'
    else:
        return 'unknown'


def replace_missing_vals(cell_entry, missing_val):
    """
    The missing value standard is "NaN". If there are other missing values present, we need to swap them.
    :param cell_entry: (str) Contents of target cell
    :param missing_val: (str)
    :return: (str)
    """
    if isinstance(cell_entry, str):
        missing_val_list = ['none', 'na', '', '-', 'n/a']
        if missing_val.lower() not in missing_val_list:
            missing_val_list.append(missing_val)
        try:
            if cell_entry.lower() in missing_val_list:
                cell_entry = 'NaN'
        except (TypeError, AttributeError):
            logging.exception("TypeError/AttributeError: replace_missing_vals()")
    return cell_entry


def extract_units(string_in):
    """
    Extract units from parenthesis in a string. i.e. "elevation (meters)"
    :param string_in: (str)
    :return: (str)
    """
    start = '('
    stop = ')'
    return string_in[string_in.index(start) + 1:string_in.index(stop)]


def extract_short(string_in):
    """
    Extract the short name from a string that also has units.
    :param string_in: (str)
    :return: (str)
    """
    stop = '('
    return string_in[:string_in.index(stop)]


# DATA WORKSHEET HELPER METHODS


def count_vars(temp_sheet, first_short):
    """
    Starts at the first short name, and counts how many variables are present
    :param temp_sheet: (obj)
    :param first_short: (int)
    :return: (int) Number of variables
    """
    count = 0
    # If we hit a blank cell, or the MV / Data cells, then stop
    while cell_occupied(temp_sheet, first_short, 0) and temp_sheet.cell_value(first_short, 0) != ("Missing" and "Data"):
        count += 1
        first_short += 1
    return count


def get_missing_val(temp_sheet):
    """
    Look for what missing value is being used.
    :param temp_sheet: (obj)
    :return: (str) Missing value
    """
    row = traverse_missing_value(temp_sheet)
    # There are two blank cells to check for a missing value
    empty = ''
    missing_val = temp_sheet.cell_value(row, 1)
    missing_val2 = temp_sheet.cell_value(row, 2)
    if cell_occupied(temp_sheet, row, 1):
        if isinstance(missing_val, str):
            missing_val = missing_val.lower()
        return missing_val
    elif cell_occupied(temp_sheet, row, 2):
        if isinstance(missing_val2, str):
            missing_val2 = missing_val2.lower()
        return missing_val2
    return empty


def traverse_short_row_int(temp_sheet):
    """
    Traverse to short name cell in data sheet. Get the row number.
    :param temp_sheet: (obj)
    :return: (int or none) Current row
    """
    for i in range(0, temp_sheet.nrows):
        # We need to keep the first variable name as a reference.
        # Then loop down past "Missing Value" to see if there is a matching variable header
        # If there's not match, then there must not be a variable header row.
        if 'Short' in temp_sheet.cell_value(i, 0):
            current_row = i + 1
            return current_row
    return


def traverse_short_row_str(temp_sheet):
    """
    Traverse to short name cell in data sheet
    :param temp_sheet: (obj)
    :return: (str or none) Name of first variable, if we find one
    """
    for i in range(0, temp_sheet.nrows):

        # We need to keep the first variable name as a reference.
        # Then loop down past "Missing Value" to see if there is a matching variable header
        # If there's not match, then there must not be a variable header row.
        if 'Short' in temp_sheet.cell_value(i, 0):
            current_row = i + 1
            ref_first_var = temp_sheet.cell_value(current_row, 0)
            return ref_first_var
    return


def traverse_missing_value(temp_sheet):
    """
    Traverse to missing value cell in data sheet
    :param temp_sheet: (obj)
    :return: (int or none) Only returns int if it finds a missing value
    """
    # Traverse down to the "Missing Value" cell. This gets us near the data we want.
    for i in range(0, temp_sheet.nrows):
        # Loop down until you hit the "Missing Value" cell, and then move down one more row
        if 'Missing' in temp_sheet.cell_value(i, 0):
            missing_row_num = i
            return missing_row_num
    return


def traverse_headers_to_data(temp_sheet, start_cell):
    """
    Traverse to the first cell that has data
    If the cell on Col 0 has content, check 5 cells to the right for content also. (fail-safe)
    :param temp_sheet: (obj)
    :param start_cell: (int) Start of variable headers
    :return: (int) First cell that contains numeric data
    """
    # Start at the var_headers row, and try to find the start of the data cells
    # Loop for 5 times. It's unlikely that there are more than 5 blank rows between the var_header row and
    # the start of the data cells. Usually it's 1 or 2 at most.
    while not cell_occupied(temp_sheet, start_cell, 0):
        start_cell += 1
    return start_cell


def traverse_mv_to_headers(temp_sheet, start):
    """
    Traverse from the missing value cell to the first occupied cell
    :param temp_sheet: (obj)
    :param start: (int) var_headers start row
    :return: (int) start cell
    """
    # Start at the var_headers row, and try to find the start of the data cells
    # Loop for 5 times. It's unlikely that there are more than 5 blank rows between the var_header row and
    # the start of the data cells. Usually it's 1 or 2 at most.
    start += 1
    # Move past the empty cells
    while not cell_occupied(temp_sheet, start, 0):
        start += 1
    # Check if there is content in first two cols
    # Move down a row, check again. (Safety check)
    num = 0
    for i in range(0, 2):
        if cell_occupied(temp_sheet, start, i):
            num += 1
    start += 1
    for i in range(0, 2):
        if cell_occupied(temp_sheet, start, i):
            num += 1
    return start


def var_headers_check(temp_sheet, missing_val_row, ref_first_var):
    """
    Check for matching variables first. If match, return var_header cell int.
    If no match, check the first two rows to see if one is all strings, or if there's some discrepancy
    :param temp_sheet: (obj)
    :param missing_val_row: (int)
    :param ref_first_var: (str)
    :return: (int) start cell
    """
    start = traverse_mv_to_headers(temp_sheet, missing_val_row)
    # If we find a match, then Variable headers exist for this file
    if temp_sheet.cell_value(start, 0) == ref_first_var:
        return start + 1
    # No var match, start to manually check the first two rows and make a best guess
    else:
        col = 0
        str_row1 = 0
        str_row2 = 0

        # Row 1
        while col < temp_sheet.ncols:
            if isinstance(temp_sheet.cell_value(start, col), str):
                str_row1 += 1
            col += 1

        # Reset variables
        col = 0
        start += 1

        # Row 2
        while col < temp_sheet.ncols:
            if isinstance(temp_sheet.cell_value(start, col), str):
                str_row2 += 1
            col += 1

        ## If the top row has more strings than the bottom row, then the top row must be the header
        if str_row1 > str_row2:
            return start
        # If not, then we probably don't have a header, so move back up one row
        else:
            return start - 1
    # If we still aren't sure, traverse one row down from the MV box and start from there
    # UNREACHABLE
    # return traverse_missing_value(temp_sheet) + 1


def cells_right_metadata_pub(workbook, sheet, row, col, pub_qty):
    """
    Specific case: We want to get all cell data for pub. Even blank cells. Necessary for creating the pub_temp list in
    cells_down_metadata()
    :param workbook: (obj)
    :param sheet: (str)
    :param row: (int)
    :param col: (int)
    :param pub_qty: (int) Number of distinct publication sections in this file
    :return: (list) Cell data for a specific row
    """
    col_loop = 0
    cell_data = []
    temp_sheet = workbook.sheet_by_name(sheet)
    while col_loop < pub_qty:
        col += 1
        col_loop += 1
        cell_data.append(temp_sheet.cell_value(row, col))
    return cell_data


def cells_right_metadata(workbook, sheet, row, col):
    """
    Traverse all cells in a row. If you find new data in a cell, add it to the list.
    :param workbook: (obj)
    :param sheet: (str)
    :param row: (int)
    :param col: (int)
    :return: (list) Cell data for a specific row
    """
    col_loop = 0
    cell_data = []
    temp_sheet = workbook.sheet_by_name(sheet)
    while col_loop < temp_sheet.ncols:
        col += 1
        col_loop += 1
        try:
            if temp_sheet.cell_value(row, col) != xlrd.empty_cell and temp_sheet.cell_value(row, col) != '':
                cell_data.append(temp_sheet.cell_value(row, col))
        except IndexError:
            pass
    return cell_data


def cells_down_metadata(workbook, sheet, row, col, finalDict):
    """
    Traverse all cells in a column moving downward. Primarily created for the metadata sheet, but may use elsewhere.
    Check the cell title, and switch it to.
    :param workbook: (obj)
    :param sheet: (str)
    :param row: (int)
    :param col: (int)
    :param finalDict: (dict)
    :return: none
    """
    row_loop = 0
    pub_cases = ['id', 'year', 'author', 'journal', 'issue', 'volume', 'title', 'pages',
                 'reportNumber', 'abstract', 'alternateCitation']
    geo_cases = ['latMin', 'lonMin', 'lonMax', 'latMax', 'elevation', 'siteName', 'location']

    # Temp Dictionaries
    pub_qty = 0
    geo_temp = {}
    general_temp = {}
    pub_temp = []
    funding_temp = []

    temp_sheet = workbook.sheet_by_name(sheet)

    # Loop until we hit the max rows in the sheet
    while row_loop < temp_sheet.nrows:
        try:
            # If there is content in the cell...
            if temp_sheet.cell_value(row, col) != xlrd.empty_cell and temp_sheet.cell_value(row, col) not in EMPTY:

                # Convert title to correct format, and grab the cell data for that row
                title_formal = temp_sheet.cell_value(row, col)
                title_json = name_to_jsonld(title_formal)

                # If we don't have a title for it, then it's not information we want to grab
                if title_json:

                    # Geo
                    if title_json in geo_cases:
                        cell_data = cells_right_metadata(workbook, sheet, row, col)
                        geo_temp = compile_temp(geo_temp, title_json, cell_data)

                    # Pub
                    # Create a list of dicts. One for each pub column.
                    elif title_json in pub_cases:

                        # Authors seem to be the only consistent field we can rely on to determine number of Pubs.
                        if title_json == 'author':
                            cell_data = cells_right_metadata(workbook, sheet, row, col)
                            pub_qty = len(cell_data)
                            for i in range(pub_qty):
                                author_lst = compile_authors(cell_data[i])
                                pub_temp.append({'author': author_lst, 'pubDataUrl': 'Manually Entered'})
                        else:
                            cell_data = cells_right_metadata_pub(workbook, sheet, row, col, pub_qty)
                            for pub in range(pub_qty):
                                if title_json == 'id':
                                    pub_temp[pub]['identifier'] = [{"type": "doi", "id": cell_data[pub]}]
                                else:
                                    pub_temp[pub][title_json] = cell_data[pub]
                    # Funding
                    elif title_json == 'agency':
                        funding_temp = compile_fund(workbook, sheet, row, col)

                    # All other cases do not need fancy structuring
                    else:
                        cell_data = cells_right_metadata(workbook, sheet, row, col)
                        general_temp = compile_temp(general_temp, title_json, cell_data)

        except IndexError:
            continue
        row += 1
        row_loop += 1

    # Compile the more complicated items
    geo = compile_geo(geo_temp)

    # Insert into final dictionary
    finalDict['@context'] = "context.jsonld"
    finalDict['pub'] = pub_temp
    finalDict['funding'] = funding_temp
    finalDict['geo'] = geo

    # Add remaining general items
    for k, v in general_temp.items():
        finalDict[k] = v

    return


def cells_right_datasheets(workbook, sheet, row, col, colListNum):
    """
    Collect metadata for one column in the datasheet
    :param workbook: (obj)
    :param sheet: (str)
    :param row: (int)
    :param col: (int)
    :param colListNum: (int)
    :return: (dict) Attributes Dictionary
    """
    temp_sheet = workbook.sheet_by_name(sheet)
    empty = ["N/A", " ", xlrd.empty_cell, "", "NA"]

    # Iterate over all attributes, and add them to the column if they are not empty
    attrDict = OrderedDict()
    attrDict['number'] = colListNum

    # Get the data type for this column
    attrDict['dataType'] = str(get_data_type(temp_sheet, colListNum))

    # Separate dict for climateInterp block
    climInDict = {}

    try:
        # Loop until we hit the right-side boundary
        while col < temp_sheet.ncols:
            cell = temp_sheet.cell_value(row, col)

            # If the cell contains any data, grab it
            if cell not in empty and "Note:" not in cell:

                title_in = name_to_jsonld(temp_sheet.cell_value(1, col))

                # Special case if we need to split the climate interpretation string into 3 parts
                if title_in == 'climateInterpretation':
                    if cell in empty:
                        climInDict['parameter'] = ''
                        climInDict['parameterDetail'] = ''
                        climInDict['interpDirection'] = ''
                    else:
                        cicSplit = cell.split('.')
                        climInDict['climateParameter'] = cicSplit[0]
                        climInDict['climateParameterDetail'] = cicSplit[1]
                        climInDict['interpDirection'] = cicSplit[2]

                # Special case to add these two categories to climateInterpretation
                elif title_in == 'seasonality' or title_in == 'basis':
                    climInDict[title_in] = temp_sheet.cell_value(row, col)

                # If the key is null, then this is a not a cell we want to add
                # We also don't want Data Type, because we manually check for the content data type later
                # Don't want it to overwrite the other data type.
                # Happens when we get to the cells that are filled with formatting instructions
                # Ex. "Climate_interpretation_code has 3 fields separated by periods..."
                elif title_in is (None or 'dataType'):
                    pass

                # Catch all other cases
                else:
                    attrDict[title_in] = cell
            col += 1

    except IndexError:
        print("Cell Right datasheets index error")

    # Only add if there's data
    if climInDict:
        attrDict['climateInterpretation'] = climInDict
    return attrDict


def cells_down_datasheets(filename, workbook, sheet, row, col):
    """
    Add measurement table data to the final dictionary
    :param filename: (str)
    :param workbook: (obj?str?)
    :param sheet: (str)
    :param row: (int)
    :param col: (int)
    :return: (dict)
    """
    # Create a dictionary to hold each column as a separate entry
    paleoDataTableDict = OrderedDict()

    # Iterate over all the short_name variables until we hit the "Data" cell, or until we hit an empty cell
    # If we hit either of these, that should mean that we found all the variables
    # For each short_name, we should create a column entry and match all the info for that column
    temp_sheet = workbook.sheet_by_name(sheet)
    columnsTop = []
    commentList = []
    colListNum = 1
    iter_var = True

    # Loop for all variables in top section
    try:
        while iter_var:

            cell = temp_sheet.cell_value(row, col).lstrip().rstrip()
            if (cell == 'Data') or (cell == 'Missing Value') \
                    or (cell == 'The value or character string used as a placeholder for missing values'):
                break
            else:
                variable = name_to_jsonld(temp_sheet.cell_value(row, col))

                # If the cell isn't blank or empty, then grab the data
                # Special case for handling comments since we want to stop them from being inserted at column level
                if variable == 'comments':
                    for i in range(1, 3):
                        if cell_occupied(temp_sheet, row, i):
                            commentList.append(temp_sheet.cell_value(row, i))

                # All other cases, create a list of columns, one dictionary per column
                elif temp_sheet.cell_value(row, col) != ('' and xlrd.empty_cell):
                    columnsTop.append(cells_right_datasheets(workbook, sheet, row, col, colListNum))
                    colListNum += 1
                row += 1

    except IndexError:
        pass

    # Add all our data pieces for this column into a new entry in the Measurement Table Dictionary
    paleoDataTableDict['paleoDataTableName'] = sheet
    paleoDataTableDict['filename'] = str(filename) + '-' + str(sheet) + ".csv"
    paleoDataTableDict['missingValue'] = 'NaN'

    # If comments exist, insert them at table level
    if commentList:
        paleoDataTableDict['comments'] = commentList[0]
    paleoDataTableDict['columns'] = columnsTop

    # Reset list back to null for next loop
    commentList = []
    return paleoDataTableDict

# CHRONOLOGY HELPER METHODS


def blind_data_capture(temp_sheet):
    """
    DEPRECATED
    This was the temporary, inconsistent way to get chron data as a whole chunk.
    :param temp_sheet: (obj)
    :return: (dict)
    """
    chronology = OrderedDict()
    start_row = traverse_to_chron_var(temp_sheet)
    for row in range(start_row, temp_sheet.nrows):
        key = str(row)
        row_list = []
        for col in range(0, temp_sheet.ncols):
            row_list.append(temp_sheet.cell_value(row, col))
        chronology[key] = row_list

    return chronology


def count_chron_variables(temp_sheet):
    """
    Count the number of chron variables
    :param temp_sheet: (obj)
    :return: (int) variable count
    """
    total_count = 0
    start_row = traverse_to_chron_var(temp_sheet)
    while temp_sheet.cell_value(start_row, 0) != '':
        total_count += 1
        start_row += 1
    return total_count


def get_chron_var(temp_sheet, start_row):
    """
    Capture all the vars in the chron sheet (for json-ld output)
    :param temp_sheet: (obj)
    :param start_row: (int)
    :return: (list of dict) column data
    """
    col_dict = OrderedDict()
    out_list = []
    column = 1

    while (temp_sheet.cell_value(start_row, 0) != '') and (start_row < temp_sheet.nrows):
        short_cell = temp_sheet.cell_value(start_row, 0)
        units_cell = temp_sheet.cell_value(start_row, 1)
        long_cell = temp_sheet.cell_value(start_row, 2)

        ## Fill the dictionary for this column
        col_dict['number'] = column
        col_dict['parameter'] = short_cell
        col_dict['description'] = long_cell
        col_dict['units'] = units_cell
        out_list.append(col_dict.copy())
        start_row += 1
        column += 1

    return out_list


def traverse_to_chron_data(temp_sheet):
    """
    Traverse down to the first row that has chron data
    :param temp_sheet: (obj)
    :return: (int) traverse_row
    """
    traverse_row = traverse_to_chron_var(temp_sheet)
    reference_var = temp_sheet.cell_value(traverse_row, 0)

    # Traverse past all the short_names, until you hit a blank cell (the barrier)
    while temp_sheet.cell_value(traverse_row, 0) != '':
        traverse_row += 1
    # Traverse past the empty cells until we hit the chron data area
    while temp_sheet.cell_value(traverse_row, 0) == '':
        traverse_row += 1

    # Check if there is a header row. If there is, move past it. We don't want that data
    if temp_sheet.cell_value(traverse_row, 0) == reference_var:
        traverse_row += 1

    return traverse_row


def traverse_to_chron_var(temp_sheet):
    """
    Traverse down to the row that has the first variable
    :param temp_sheet: (obj)
    :return: (int)
    """
    row = 0
    while row < temp_sheet.nrows - 1:
        if 'Parameter' in temp_sheet.cell_value(row, 0):
            row += 1
            break
        row += 1

    return row


def get_chron_data(temp_sheet, row, total_vars):
    """
    Capture all data in for a specific chron data row (for csv output)
    :param temp_sheet: (obj)
    :param row: (int)
    :param total_vars: (int)
    :return: (list) data_row
    """

    data_row = []
    missing_val_list = ['none', 'na', '', '-']
    for i in range(0, total_vars):
        cell = temp_sheet.cell_value(row, i)
        if isinstance(cell, str):
            cell = cell.lower()
        if cell in missing_val_list:
            cell = 'NaN'
        data_row.append(cell)
    return data_row


if __name__ == '__main__':
    excel()
