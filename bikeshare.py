import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_list = ['chicago','nyc','washington']
month_list = ['january','february','march','april','may','june','all']
day_list = ['monday','tuesday','wednesday','thursady','friday','saturday','sunday','all']

welcome_pic = """-----__o------
----_\ <,_----
---(_)/ (_)---"""

chicago_pic = """-----
 ☆☆☆☆☆
 -----
"""

nyc_pic = """  /
 /\//\\
 ||
 \___/
"""

washington_pic = """☆ ☆ ☆
 -----
 -----
"""

CITY_PICS = { 'chicago': chicago_pic,
              'nyc': nyc_pic,
              'washington': washington_pic }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print(welcome_pic)
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input("Choose a city (Chicago, NYC, or Washington): ")).lower()
    while city not in city_list:
        city = str(input("Mistake! Choose a coreect city from the list (Chicago, NYC, or Washington): ")).lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = str(input("Choose a month from January to June or choose All): ")).lower()
    while month not in month_list:
        month = str(input("Mistake! Choose a correct month from January to June or choose All): ")).lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input("Choose a day of the week (full name or choose All): ")).lower()
    while day not in day_list:
        day = str(input("Mistake! Choose a correct day of the week (full name or choose All): ")).lower()

    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

# TO DO: check if show or not raw data
def show_raw_data(df):
    print('Do you want to see raw data? (Y/N)')
    raw_data = input("Your choice: ").lower()
    if raw_data == "y":
        i = input("How many rows would you like to see? (if not number is input, you will see 5 rows) ")

        try:
            k = int(i)
        except(ValueError):
            i = 5
        else:
            i = k

        st = 0
        e = int(i)

        message = '\nWould you like to see ' + str(i) + ' more lines? Enter Y or N.\n'
        while True:
            print(df[st:e])
            st += int(i)
            e += int(i)
            more = input(message)
            if more.lower() != 'y':
                break
        print('-'*40)
    else:
        print('-'*40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month is", popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day of week is", popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most common start hour is", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("The most common start station is", popular_start)

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("The most common end station is", popular_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + " -> " + df['End Station']
    popular_route = df['route'].mode()[0]
    print("The most common route is", popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    total_time_sec = int(total_time % 60)
    total_time_mins = int((total_time // 60) % 60)
    total_time_hours = int(((total_time // 60) // 60) % 24)
    total_time_days = int(((total_time // 60) // 60) // 24)
    print("The total biking time is", total_time, "seconds, or",total_time_days,"days,",total_time_hours,"hours,",total_time_mins,"minutes and",total_time_sec,"seconds")

    # TO DO: display mean travel time
    average_time = int(df['Trip Duration'].mean())
    average_time_sec = int(average_time % 60)
    average_time_mins = int(average_time // 60)
    print("The average biking time is", average_time, "seconds, or",average_time_mins,"minutes and",average_time_sec,"seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types and gender
    df['Gender Type'] = df['Gender']+df['User Type']
    male_subscriber = df[df['Gender Type'] == 'MaleSubscriber'].count()[1]
    male_customer = df[df['Gender Type'] == 'MaleCustomer'].count()[1]
    female_subscriber = df[df['Gender Type'] == 'FemaleSubscriber'].count()[1]
    female_customer = df[df['Gender Type'] == 'FemaleCustomer'].count()[1]
    total_male = male_subscriber + male_customer
    total_female = female_subscriber + female_customer
    total_subscriber = female_subscriber + male_subscriber
    total_customer = female_customer + male_customer
    total_riders = total_subscriber + total_customer

    # TO DO: Display counts of absolute numbers

    cohorts_stats = {
    'Female': pd.Series([female_subscriber,female_customer,total_female], index = ['Subsriber','Customer','Total']),
    'Male': pd.Series ([male_subscriber,male_customer,total_male], index = ['Subsriber','Customer','Total']),
    'Total': pd.Series([total_subscriber,total_customer,total_riders], index = ['Subsriber','Customer','Total'])}

    cohorts_visual=pd.DataFrame(cohorts_stats)

    print(cohorts_visual,"\n")

    # TO DO: Display counts of share

    cohorts_per = {
    'Female': pd.Series([female_subscriber/total_subscriber*100,female_customer/total_customer*100,total_female/total_riders*100], index = ['Subsriber','Customer','Total']),
    'Male': pd.Series ([male_subscriber/total_subscriber*100,male_customer/total_customer*100,total_male/total_riders*100], index = ['Subsriber','Customer','Total']),
    'Total': pd.Series([total_subscriber/total_riders*100,total_customer/total_riders*100,''], index = ['Subsriber','Customer','Total'])}

    cohorts_visual_per=pd.DataFrame(cohorts_per)

    print(cohorts_visual_per,"\n")


    # TO DO: Display earliest, most recent, and most common year of birth
    oldest = int(df['Birth Year'].min())
    youngest = int(df['Birth Year'].max())
    popular_year = int(df['Birth Year'].mode())
    mean_age = 2021 - int(df['Birth Year'].mode())
    print("The oldest rider was born in", oldest, "year")
    print("The younger rider was born in", youngest, "year")
    print("The most common riders' year of birth is", popular_year, "while the mean rider age is", mean_age)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        city_pic = CITY_PICS[city]

        print("\n", "Your city is:", city.title(), "\n", city_pic, "Your month is:", month.title(), "\n", "Your day is:", day.title(), "\n")

        show_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        if city != 'washington':
            user_stats(df)
        else:
            '\n'

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
