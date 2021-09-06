import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    user_input_city = "invalid"
    valid_cities = ["chicago", "new york city", "washington"]
    while user_input_city is "invalid":
        city=input("Please enter a city to analyse. Your choices are Chicago (C), New York City (N) or Washington (W): ").lower()
        for i in valid_cities:
            if city == i[:1] or city == i:
                city = i
                user_input_city = "valid"
        if user_input_city == "invalid":
            print("Input was not valid")
    print("You have selected {}.".format(city.title()))
    # TO DO: get user input for month (all, january, february, ... , june)
    user_input_month = "invalid"
    valid_months = ["all", "january", "february", "march", "april", "may", "june"]
    while user_input_month == "invalid":
        month = input("Please enter the month or three letter abbreviation of the month you would like to explore between January and June. If you would like to view all months, please type \"all\": ").lower()
        for i in valid_months:
            if month == i[:3] or month == i:
                month = i
                user_input_month = "valid"
        if user_input_month == "invalid":
            print("Input was not valid")
    print("You have selected {}.".format(month.title()))
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    user_input_day = "invalid"
    valid_days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    while user_input_day == "invalid":
        day = input("Please enter the day or three letter abbreviation of the day you would like to explore. If you would like to view all days, please type \"all\": ").lower()
        for i in valid_days:
            if day == i[:3] or day == i:
                day = i
                user_input_day = "valid"
        if user_input_day == "invalid":
            print("Input was not valid.")
    print("You have selected {}.".format(day.title()))
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
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["Month"] = df["Start Time"].dt.month
    df["Day of Week"] = df["Start Time"].dt.dayofweek
    df["Hour"] = df["Start Time"].dt.hour
    months = ["january", "february", "march", "april", "may", "june"]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if month != "all":
        month = months.index(month)+1
        df=df[df.Month==month]
    if day != "all":
        day = days.index(day)
        df=df[df["Day of Week"]==day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    months = ["january", "february", "march", "april", "may", "june"]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df["Month"].mode()[0]
    print("The most common month is {}.".format(months[popular_month-1].title()))

    # TO DO: display the most common day of week
    popular_day = df["Day of Week"].mode()[0]
    print("The most common day of the week is {}.".format(days[popular_day].title()))

    # TO DO: display the most common start hour
    popular_hour = df["Hour"].mode()[0]
    popular_hour_12 = 12
    popular_hour_am_pm = "pm"
    if popular_hour < 12:
        popular_hour_12 = popular_hour
        popular_hour_am_pm = "am"
    elif popular_hour > 12:
        popular_hour_12 = popular_hour - 12
        popular_hour_am_pm = "pm"


    print("The most common start hour was {}, i.e. {} {}.".format(popular_hour, popular_hour_12, popular_hour_am_pm))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df["Start Station"].mode()[0]
    print("The most popular starting station is {}.".format(popular_start))

    # TO DO: display most commonly used end station
    popular_end = df["End Station"].mode()[0]
    print("The most popular end station is {}.".format(popular_end))

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = (df["Start Station"] + " to " + df["End Station"]).mode()[0]
    print("The most popular trip is from {}.".format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df["End Time"] =pd.to_datetime(df["End Time"])
    df["Trip Duration"]=df["End Time"] - df["Start Time"] # I have made the assumption here that end time is after start time. Testing my program I can see that this is not always the case (Print 10 rows of data for washington for Sundays in April for an example), however I am not sure if fixing this is within course scope.
    total_time = df["Trip Duration"].sum()
    total_time_days = total_time.days
    total_time_hours = total_time.seconds//3600
    total_time_minutes = (total_time.seconds - 3600*total_time_hours)//60
    total_time_seconds = total_time.seconds - (total_time_hours*3600 + total_time_minutes*60)
    print("The total travel time for all bikes was {} days, {} hours, {} minutes, and {} seconds.".format(total_time_days, total_time_hours, total_time_minutes, total_time_seconds))

    # TO DO: display mean travel time
    average_time = df["Trip Duration"].mean()
    average_time_minutes = average_time.days*24*60 + average_time.seconds//60
    average_time_seconds = average_time.seconds - (average_time_minutes*60)
    print("The average trip time was {} minutes, and {} seconds.".format(average_time_minutes, average_time_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The breakdown of user types is: ")
    print(df["User Type"].value_counts())



    # TO DO: Display counts of gender TO DO: Display earliest, most recent, and most common year of birth
    if city == "new york city" or city == "chicago":
        print("The breakdown of genders is: ")
        print(df["Gender"].value_counts(dropna=False))
        print("The earliest year of birth is {}.".format(int(df["Birth Year"].min())))
        print("The latest year of birth is {}.".format(int(df["Birth Year"].max())))
        print("The most common year of birth is {}.".format(int(df["Birth Year"].mode()[0])))
    elif city == "washington":
        print("Gender and Year of Birth data is not available for Washington.")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_data(df, start_row): #This function asks the user to provide a number of rows to display, and displays that many additional rows
    pd.set_option('display.max_columns',200)
    if start_row == 0:
        data_view = input("Would you like to see rows of the original data (Y/N)? ").lower()[0]
        if data_view != "y":
            return
    row_increment_int = ""
    while True:
        row_increment = input("How many rows would you like to see? ")
        try:
            row_increment_int = int(row_increment)
            break
        except:
            print("Please enter a valid integer")
    print(df.head(row_increment_int+start_row).tail(row_increment_int))
    data_view = input("Would you like to see more rows of the original data (Y/N)? ").lower()[0]
    if data_view != "y":
        return
    print_data(df,row_increment_int+start_row)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        print_data(df, 0)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
