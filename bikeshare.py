import datetime
import time
import pandas as pd
# import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
DEBUG = 0
# =============================================================================
# Header information block:
# acronym Date     company, name
# description
# =============================================================================
# MDO001  20191231 Bayer Business Services, Markus Dolhaine
# Introduction to Python, Project: Explore US Bikeshare Data
# a) general remarks
# Single quotes will be used throughout this script as string delimiters -
# single quotes within strings will be escaped appropriately.
#
# =============================================================================


def get_filters():  # done
    '''
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
            or 'all' to apply no month filter
            (str) day - name of the day of week to filter by,
            or 'all' to apply no day filter
    '''

    # default values:
    month = 'all'
    day = 'all'

    # some simple strings to be reused:
    sorry_prompt = 'Sorry, I might have misunderstood your answer.\n'
    cancel_prompt = '(X to cancel the program)\n'

    cancel_pgm = False
    print('Hello! Let\'s explore some US bikeshare data!')
    initial_prompt = ('Which city\'s data do you want to analyze? '
                      'Please enter Chicago, New York City, or Washington '
                      '(abbreviations accepted):\n')
    # Get user input for city (chicago, new york city, washington).
    # Not mentioned in the prompt, but 'NY' or 'NYC' are allowed as
    # abbreviations as well
    city = input(initial_prompt).lower()
    while city not in ['chicago', 'new york city', 'ny', 'nyc', 'washington']:
        # Any invalid user input results in repeating the question.
        # Entering an X will terminate all user entry and stop the program w/o
        # any display of outputs
        if DEBUG:
            print(city)
        prompt = (sorry_prompt + initial_prompt + cancel_prompt)
        city = input(prompt).lower()
        if city == 'x':
            cancel_pgm = True
            break

    if not cancel_pgm:
        # If abbreviations were used by the user, these have to be expanded to
        # the full city name.
        if city in ('ny', 'nyc'):
            city = 'new york city'
        print('\n', '-'*66, '\nGreat, you\'ve selected', city.title(),
              'for analysis, let\'s keep going\n', '-'*66)

    # get user input for month (all, january, february, ... , june)
    if not cancel_pgm:
        MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june']
        valid_months = ['1', '2', '3', '4', '5', '6',
                        'ja', 'f', 'fe', 'feb', 'mar',
                        'ap', 'apr', 'may', 'j', 'ju', 'jun',
                        'january', 'february', 'march', 'april', 'may', 'june',
                        'n', 'no', 'none', 'nothing', 'all']
        initial_prompt = ('Which month\'s data do you want to analyze?\n'
                          'Please enter a month name (abbreviations accepted) '
                          'or a number:\n')
        month = input(initial_prompt).lower()
        while month not in valid_months:
            prompt = (sorry_prompt + initial_prompt + cancel_prompt)
            month = input(prompt).lower()
            if month == 'x':
                cancel_pgm = True
                break
    if not cancel_pgm:
        # If abbreviations were used by the user,
        # these have to be expanded to the full month name.
        if month[:2] == 'ja':
            month = MONTH_DATA[0]
        elif month[:1] == 'f':
            month = MONTH_DATA[1]
        elif month[:3] == 'mar':
            month = MONTH_DATA[2]
        elif month[:2] == 'ap':
            month = MONTH_DATA[3]
        elif month[:3] == 'may':
            month = MONTH_DATA[4]
        elif month[:1] == 'j':
            month = MONTH_DATA[5]
        elif month in ['1', '2', '3', '4', '5', '6']:
            month = MONTH_DATA[int(month)-1]
        else:
            month = 'all'
    if DEBUG:
        print(month.title())
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if not cancel_pgm:
        DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday',
                    'friday', 'saturday', 'sunday']
        valid_days = ['1', '2', '3', '4', '5', '6', '7',
                      'm', 'mo', 'tu', 'w', 'we', 'th', 'f', 'fr', 'sa', 'su',
                      'monday', 'tuesday', 'wednesday', 'thursday',
                      'friday', 'saturday', 'sunday',
                      'n', 'no', 'none', 'nothing', 'a', 'all']
        initial_prompt = ('Which weekday\'s data do you want to analyze?\n'
                          'Please enter a day name (abbreviations accepted) '
                          'or a number (1 = Monday):\n')
        day = input(initial_prompt)
        while day.lower() not in valid_days:
            prompt = (sorry_prompt + initial_prompt + cancel_prompt)
            day = input(prompt)
            if day.lower() == 'x':
                cancel_pgm = True
                break
    if not cancel_pgm:
        # If abbreviations were used by the user,
        # these have to be expanded to the full day name.
        if day[:1] == 'm':
            day = DAY_DATA[0]
        elif day[:2] == 'tu':
            day = DAY_DATA[1]
        elif day[:1] == 'w':
            day = DAY_DATA[2]
        elif day[:2] == 'th':
            day = DAY_DATA[3]
        elif day[:1] == 'f':
            day = DAY_DATA[4]
        elif day[:2] == 'sa':
            day = DAY_DATA[5]
        elif day[:2] == 'su':
            day = DAY_DATA[6]
        elif day in ['1', '2', '3', '4', '5', '6', '7']:
            day = DAY_DATA[int(day)-1]
        else:
            day = 'all'
    if DEBUG:
        print(day.title())

    print('-' * 40)
    return city, month, day, cancel_pgm


def load_data(city, month, day):  # done
    '''
        Loads data for the specified city
            and filters by month and day if applicable.
        Args:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by,
                or 'all' to apply no month filter
                (str) day - name of the day of week to filter by,
                or 'all' to apply no day filter
        Returns:
            df - Pandas DataFrame containing city data filtered by month / day
    '''
    cancel_pgm = False
    if DEBUG:
        print(city, month, day)
        print(CITY_DATA.get(city))
    print('\nLoading the selected data file...\n')
    start_time = time.time()
    try:
        df = pd.read_csv(CITY_DATA.get(city))
    except Exception:
        cancel_pgm = True
        print('Data load failed for file ', CITY_DATA.get(city))
    print('\nThis took %s seconds.' % round((time.time() - start_time), 6))

    # calculating additional columns that will help with statistics
    if not cancel_pgm:
        print('\nPreparing data for statistic evaluations...\n')
        start_time = time.time()
        df.insert(2, 'StartDateTime',
                  pd.to_datetime(df['Start Time'], yearfirst=True))
        if DEBUG:
            print(type(df['StartDateTime'].dt.month_name().str.lower()))
        try:
            df.insert(3, 'StartMonth',
                      df['StartDateTime'].dt.month_name().str.lower())
            df.insert(4, 'StartDay',
                      df['StartDateTime'].dt.day_name().str.lower())
            df.insert(5, 'StartHour',
                      df['StartDateTime'].dt.hour)
            df.insert(10, 'Stations',
                      'From "' + df['Start Station']
                      + '" to "' + df['End Station'] + '"')
        except Exception:
            cancel_pgm = True
            print('Inserting additional, calculated columns'
                  ' failed for dataframe\n')
        print('\nThis took %s seconds.' % round((time.time() - start_time), 6))

    # filtering data
    if not cancel_pgm:
        print('\nFiltering data according to the choices you made...\n')
        start_time = time.time()
        if DEBUG:
            print('# of rows before filtering:', df.shape[0])
        try:
            if month != 'all':
                df = df[df.StartMonth == month]
            if DEBUG:
                print('# of rows after filtering months:', df.shape[0])
            if day != 'all':
                df = df[df.StartDay == day]
            if DEBUG:
                print('# of rows after filtering days:', df.shape[0])
        except Exception:
            cancel_pgm = True
            print('Filtering the data frame by month failed, termination now!')
        if DEBUG:
            print('\nColumns:')
            print(df.columns)
        print('\nThis took %s seconds.'
              % round((time.time() - start_time), 6))

    '''
    this section of code was used to
    do a first data analysis during development!
        print(df.head())  # view the first few rows of the dataset!
        print('\nColumns:')
        print(df.columns)
        print('\ndescribe:')
        print(df.describe())
        print('\ninfo:')
        print(df.info())
        print(df['Birth Year'].value_counts())
        print(df['StartMonth'].unique())
        print(df['StartDay'].unique())
        print(df['StartHour'].unique())
        print(df['Stations'].unique())
        print(df.iloc[1]['StartMonth'])
    '''
    return df, cancel_pgm
    print('\nThis took %s seconds.' % round((time.time() - start_time), 6))


def time_stats(df, month, day):  # done
    """
        Displays statistics on the most frequent times of travel
    """
    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()
    # repeating the filters for information of the user
    print('(You filtered for month = {} and day = {})\n'.format(month, day))
    # display the most common month
    most_common_start_month = df['StartMonth'].mode()
    print('Most popular month: \t{}'.format(most_common_start_month[0]))
    # display the most common day of week
    most_common_start_day = df['StartDay'].mode()
    print('Most popular day: \t{}'.format(most_common_start_day[0]))
    # display the most common start hour
    most_common_start_hour = df['StartHour'].mode()
    print('Most popular hour: \t{}'.format(most_common_start_hour[0]))
    print('\nThis took %s seconds.' % round((time.time() - start_time), 6))
    print('-' * 40)


def station_stats(df):  # done
    ''' Displays statistics on the most popular stations and trip. '''
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()
    print('Most popular start station: \t{}'.format(
        most_common_start_station[0]))
    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()
    print('Most popular end station: \t{}'.format(most_common_end_station[0]))
    # display most frequent combination of start station and end station trip
    most_common_trip = df['Stations'].mode()
    print('Most popular trip: \t\t{}'.format(most_common_trip[0]))
    print('\nThis took %s seconds.' % round((time.time() - start_time), 6))
    print('-' * 40)


def trip_duration_stats(df):  # done
    ''' Displays statistics on the total and average trip duration. '''
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travels
    total_travels = df['Trip Duration'].count()
    print('The total number of travels: \t\t', f'{total_travels:,}')
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    sec = datetime.timedelta(seconds=int(total_travel_time))
    d = datetime.datetime(1, 1, 1) + sec
    print('The total travel durations (in seconds):',
          f'{total_travel_time:,}')
    print('The total travel durations (formatted) :',
          f'{total_travel_time // 86400:,}',
          'Days, %d Hours, %d Minutes, and %d Seconds'
          % (d.hour, d.minute, d.second))
    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('The average travel duration (in seconds):',
          f'{average_travel_time}')
    print('\nThis took %s seconds.' % round((time.time() - start_time), 6))
    print('-' * 40)


def user_stats(df, city):
    ''' Displays statistics on bikeshare users. '''
    washington_msg = ' data is not available for the city of Washington!'
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print('The users are split as follows:\n',
          df['User Type'].value_counts().to_frame(), '\n')
    # Display counts of gender
    if city == 'washington':
        print('Gender' + washington_msg)
    else:
        print('The gender distribution is as follows:\n',
              df['Gender'].value_counts().to_frame(), '\n')
    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('Birth Year' + washington_msg)
    else:
        print('The earliest Year of Birth\t: ', int(df['Birth Year'].min()))
        print('The most recent Year of Birth\t: ', int(df['Birth Year'].max()))
        most_common_yob = df['Birth Year'].mode()
        print('The most common Year of Birth\t: ', int(most_common_yob[0]))
    print('\nThis took %s seconds.' % round((time.time() - start_time), 6))
    print('-' * 40)


def show_raw_data(df):
    # some simple strings to be reused:
    sorry_prompt = 'Sorry, I might have misunderstood your answer.\n'
    cancel_prompt = '(X to cancel the program)\n'

    cancel_pgm = False
    initial_prompt = ('Would you like to see individual trip data '
                      + '(five "more" rows at a time)  (yes/no)?\n')
    starting_row = 0
    while True:
        show_raw = input(initial_prompt).lower()
        while show_raw not in ['y', 'yes', 'n', 'no', 'x']:
            prompt = (sorry_prompt + initial_prompt + cancel_prompt)
            show_raw = input(prompt).lower()
        if show_raw in ['yes', 'y']:
            for i in range(0, 5):
                print('\nRecord with index: ', end='')
                print(df.iloc[i + starting_row].to_frame())
            print('\nRecord numbers shown are the ones '
                  'from the original data file')
            print('Gaps in record numbers are due '
                  'to the filtering you requested')
            starting_row += 5
        elif show_raw == 'x':
            cancel_pgm = True
            break
        else:
            break
    return cancel_pgm


def main():
    cancel_pgm = False
    while not cancel_pgm:
        city, month, day, cancel_pgm = get_filters()
        if cancel_pgm:
            break
        df, cancel_pgm = load_data(city, month, day)
        if cancel_pgm:
            break
        time_stats(df, month, day)
        input('Please press return to continue ...')
        station_stats(df)
        input('Please press return to continue ...')
        trip_duration_stats(df)
        input('Please press return to continue ...')
        user_stats(df, city)
        cancel_pgm = show_raw_data(df)
        if cancel_pgm:
            break
        initial_prompt = '\nWould you like to restart (yes/no)?\n'
        restart = input(initial_prompt).lower()
        while restart not in ['y', 'yes', 'n', 'no', 'x']:
            prompt = ('\nSorry, I might have misunderstood your answer'
                      + initial_prompt + '(X to cancel the program)\n')
            restart = input(prompt).lower()
        if restart not in ['yes', 'y']:
            break
    print('Thanks for your time, good bye!')


if __name__ == '__main__':
    main()
