import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# creating options to display for users to select a city
city_options = {i: city for i, city in enumerate(CITY_DATA.keys(), 1)}

city_check = 'Select the number corresponding to the city of your choice.\n'
for i, city in city_options.items():
    city_check += f'\t{i} {city}\n'


filter_check = 'Select an option to filter either by month, day, both or none.\n\t1. Months\n\t2. Day of the week\n\t3. Both\n\t4. No filter (view all data)\n'

def choose_city():
    valid_city_input = False
    trials = 0

    while not valid_city_input:
        time.sleep(1)
        if trials > 0:
            print('Ensure the number you select is an available option.')
            time.sleep(1)
        try:
            value = int(input(city_check))
            if value in city_options.keys():
                valid_city_input = True
                city = city_options[value]
        except ValueError:
            print('You can only type in numbers(in figures) that correspond to your choice. Example 1, 2, 3...')
        trials += 1

    return city

def choose_month():
    months = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
    ]
    valid_month_input = False
    month_trials = 0
    
    while not valid_month_input:
        if month_trials > 0:
            print('Hint: check spellings')
        time.sleep(1)
        month = input('type in the month you want to view: ').strip().capitalize()
        if month in months:
            valid_month_input = True
        month_trials += 1

    return month

def choose_day_of_week():
    week_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    valid_weekday_input = False
    weekday_trials = 0

    while not valid_weekday_input:
        if weekday_trials > 0:
            print('Hint: check spellings')
        time.sleep(1)
        day = input('type in the day of the week you want to view: ').strip().capitalize()
        if day in week_days:
            valid_weekday_input = True
        weekday_trials += 1

    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    valid_filter_input = False
    # select city
    city = choose_city()

    # select filter option.
    while not valid_filter_input:    
        filter_input = input(filter_check)
        if filter_input == '1':
            month = choose_month()
            day = 'All'
            valid_filter_input = True
        elif filter_input == '2':
            month = 'All'
            day = choose_day_of_week()
            valid_filter_input = True
        elif filter_input == '3':
            month = choose_month()
            day = choose_day_of_week()
            valid_filter_input = True
        elif filter_input == '4':
            month = 'All'
            day = 'All'
            valid_filter_input = True
        else:
            print('You can only type in numbers(in figures) that correspond to your choice. Example 1, 2, 3...')
            time.sleep(1)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city], index_col=[0])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month_name()
    df['day of week'] = df['Start Time'].dt.day_name()

    if month.capitalize() != 'All':
        df = df[df['month'] == month]
    if day.capitalize() != 'All':
        df = df[df['day of week'] == day]
    
    return df


def time_stats(df):
    sleep = 2
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(f'The most common month traveled is {most_common_month}')
    time.sleep(sleep)
    
    # display the most common day of week
    most_common_week = df['day of week'].mode()[0]
    print(f'The most common day of the week traveled is {most_common_week}')
    time.sleep(sleep)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f'The most common starting hour of travel is {most_common_hour}')
    time.sleep(sleep)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(sleep)


def station_stats(df):
    sleep = 2
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print(f'The most commonly used start station is {most_start_station}')
    time.sleep(sleep)

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print(f'The most commonly used end station is {most_end_station}')
    time.sleep(sleep)

    # display most frequent combination of start station and end station trip
    combined_series = df['Start Station'].value_counts() + df['End Station'].value_counts()
    combined_series.sort_values(inplace=True)
    most_frequent_station = combined_series.idxmax()
    print(f'The most frequently used station(start and end combined) is {most_frequent_station}')
    time.sleep(sleep)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(sleep)


def trip_duration_stats(df):
    sleep = 2
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'The total travel time is {total_travel_time}')
    time.sleep(sleep)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'The average travel time is calculated to be {mean_travel_time}')
    time.sleep(sleep)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(sleep)


def user_stats(df):
    sleep = 2
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f'The number of each user type in the dataset is represented below: ')
    for i, item in df['User Type'].value_counts().items():
        print(i, item)
    time.sleep(sleep)

    print('\n')
    
    # Display counts of gender
    try:
        counts_of_gender = df['Gender'].value_counts()
        number_of_NaNs = df['Gender'].isna().sum()
        male_count = counts_of_gender['Male']
        female_count = counts_of_gender['Female']

        print(f'{number_of_NaNs} Gender informatons were not provided and hence ignored in this analysis')
        time.sleep(1)
        print(f'The number of male and female users are represented as: ')
        for i, item in df['Gender'].value_counts().items():
            print(i, item)
        time.sleep(1)
        print(f'There are {counts_of_gender.sum()} gender information provided in total')        
        time.sleep(1)    
    except KeyError:
        print('There is no data for gender in this file.')
    time.sleep(sleep)

    print('\n')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print(f'The earliest birth year is {earliest}')
        time.sleep(1)
        print(f'The most recent birth year is {most_recent}')
        time.sleep(1)
        print(f'The most common birth year is {most_common}')
        time.sleep(1)
    except KeyError:
        print('There is no data for birth year of users in this data set')
    time.sleep(sleep)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(sleep)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
