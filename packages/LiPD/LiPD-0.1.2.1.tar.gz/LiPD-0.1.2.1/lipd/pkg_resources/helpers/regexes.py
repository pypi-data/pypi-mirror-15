import re

"""
GLOBAL LIST OF REGEXES
"""

# DOI
DOI = re.compile(r'\b(10[.][0-9]{3,}(?:[.][0-9]+)*/(?:(?!["&\'<>,])\S)+)\b')

# NOAA
# Convert camelCase to underscore
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')
RE_VAR = re.compile(r'#{2}(\w)+')
RE_VAR_SPLIT = re.compile(r'(\w+)(\s+)([\w\W\s]+)')


# TIMESERIES Convert
re_misc_fetch = re.compile(r'(geo_(\w+)|climateInterpretation_(\w+)|calibration_(\w+)|paleoData_(\w+))')
re_pub_fetch = re.compile(r'pub1_(citation|year|DOI|author|publisher|title|type|volume|issue|journal|link|pubDataUrl|abstract|pages)')

re_pub_valid = re.compile(r'pub(\d)_(citation|year|DOI|author|publisher|title|type|volume|issue|journal|link|pubDataUrl|abstract|pages)')
re_fund_valid = re.compile(r'funding(\d)_(grant|agency)')

re_pub_invalid = re.compile(r'pub_(\w+)|pub(\d)_(\w+)|pub(\d)(\w+)|pub(\w+)')
re_fund_invalid = re.compile(r'agency|grant|funding_agency|funding_grant')
re_geo_invalid = re.compile(r'geo(\w+)|geo_(\w+)')
re_paleo_invalid = re.compile(r'paleodata(\w+)|paleodata_(\w+)|measurement(\w+)|measurement_(\w+)')
re_calib_invalid = re.compile(r'calibration(\w+)|calibration_(\w+)')
re_clim_invalid = re.compile(r'climateinterpretation(\w+)|climateinterpretation_(\w+)')

re_pub_nh = re.compile(r'pub(\d)_(\w+)')
re_pub_cc = re.compile(r'pub(\w+)')
re_pub_h = re.compile(r'pub_(\w+)')
re_pub_n = re.compile(r'pub(\d)(\w+)')

# START
# re_filter_expr = re.compile(r"((\w+_?)\s*(is|in|greater than|equals|equal|less than|<=|==|>=|=|>|<){1}[\"\s\']*([\"\w\d]+|-?\d+.?\d*)[\"\s&\']*)")
re_filter_expr = re.compile(r"((\w+_?)\s*(is|in|greater than|equals|equal|less than|<=|==|>=|=|>|<){1}[\"\s\']*([\"\s\w\d]+|-?\d+.?\d*)[\"\s&\']*)")

# PANDAS
re_pandas_x_num = re.compile(r"(year\d?|age\d?|depth\d?)\b")
re_pandas_x_und = re.compile(r"(year|age|depth){1}[_]{1}.*")