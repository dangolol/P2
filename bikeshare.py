import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new-york-city.csv',
             'washington': 'washington.csv'}
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
WEEKDAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

# Data columns:  Start Time, End Time, Trip Duration, Start Station, End Station, User Type, Gender, Birth Year

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter the name of city(chicago, new york city, washington): ').lower()

        if city == 'new york city' \
                or city == 'new york' \
                or city == 'ny':
            city = 'new york city'
            break
        elif city == 'chicago' \
                or city == 'chi':
            city = 'chicago'
            break
        elif city == 'washington' \
                or city == 'd.c.' \
                or city == 'd.c' \
                or city == 'dc':
            city = 'washington'
            break

        print('\nYou enter WRONG NAME OF CITY!\n')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please enter the month(all, january, february, ... , june): ').lower()

        if month in MONTHS:
            break

        print('\nYou enter WRONG MONTH\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter the name of week(all, monday, tuesday, ... sunday): ').lower()

        if day in WEEKDAYS:
            break

        print('\nYou enter WRONG NAME OF WEEK\n')

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('Most Frequent Month:', MONTHS[popular_month].title())

    # display the most common day of week
    if day == 'all':
        popular_weekday = df['day_of_week'].mode()[0]
        print('Most Frequent Day of Week:', popular_weekday)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Frequent Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Frequent End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_combination_station = (df['Start Station'] + '|' + df['End Station']).mode()[0]
    print('Most Frequent combination Station: \n    Start: '
          + popular_combination_station.split('|')[0] + '\n    End: '
          + popular_combination_station.split('|')[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('User Total Travel Time: %ds' % total_travel_time)

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('User Average Travel Time: %ds' % average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    for key in df['User Type'].unique():
        print('Counts of %s : %d' % (key, df['User Type'].value_counts()[key]))

    # Display counts of gender
    if city != 'washington':
        print('\nCounts of Male : %d' % df['Gender'].value_counts()['Male'])
        print('Counts of Female : %d' % df['Gender'].value_counts()['Female'])

    # TODO: Display earliest, most recent, and most common year of birth
        print('\nThe Earliest Year of Birth: ', int(df['Birth Year'].min()))
        print('The Most Recent Year of Birth: ', int(df['Birth Year'].max()))
        print('The Most Common Year of Birth: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
