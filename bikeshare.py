
import time

import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

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
    # Load data for the specified city
    df = pd.read_csv(CITY_DATA[city.lower()])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the month to filter data
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print(f"Most common month: {months[common_month - 1]}")

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"Most common day of the week: {common_day}")

    # Display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f"Most common hour of the day: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station: {common_start_station}")

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station: {common_end_station}")

    # Display most frequent combination of start station and end station trip
    df['start_end_combo'] = df['Start Station'] + " to " + df['End Station']
    common_start_end_combo = df['start_end_combo'].mode()[0]
    print(f"Most common trip: {common_start_end_combo}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def format_duration(seconds):
    """
    Convert duration from seconds to years, months, days, hours, minutes, and seconds.

    Args:
        (int) seconds - duration in seconds
    Returns:
        (str) formatted_duration - duration in the format of years, months, days, hours, minutes, and seconds
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    months, days = divmod(days, 30)  # Approximate duration for simplicity
    years, months = divmod(months, 12)

    formatted_duration = ""
    if years:
        formatted_duration += f"{years} years, "
    if months:
        formatted_duration += f"{months} months, "
    if days:
        formatted_duration += f"{days} days, "
    if hours:
        formatted_duration += f"{hours} hours, "
    if minutes:
        formatted_duration += f"{minutes} minutes, "
    formatted_duration += f"{seconds} seconds"

    return formatted_duration


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    formatted_total_time = format_duration(total_travel_time)
    print(f"Total travel time: {formatted_total_time}")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    formatted_mean_time = format_duration(int(mean_travel_time))
    print(f"Average travel time: {formatted_mean_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data
        city - City for which data is analyzed
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of each user type:\n", user_types)

    # For NYC and Chicago, display counts of gender and stats on birth year
    if city.lower() in ['new york city', 'chicago']:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of each gender:\n", gender_counts)

        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        
        print("\nEarliest year of birth:", int(earliest_birth_year))
        print("Most recent year of birth:", int(most_recent_birth_year))
        print("Most common year of birth:", int(most_common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """
    Asks user if they want to see raw data and displays it if they do.

    Args:
        df - Pandas DataFrame containing city data
    """
    start_index = 0
    end_index = 5

    while True:
        show_data = input("Would you like to see the raw data? Enter 'yes' or 'no': ").lower()
        if show_data == 'yes':
            print(df.iloc[start_index:end_index])
            start_index += 5
            end_index += 5
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city in cities:
            break
        else:
            print("Invalid input. Please choose either Chicago, New York City, or Washington.")

    # Get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Would you like to filter the data by month, day, or not at all? Type 'all' for no month filter. ").lower()
        if month in months:
            break
        else:
            print("Invalid input. Please choose a month between January and June, or type 'all'.")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Which day? Type 'all' for no day filter. ").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please choose a day of the week, or type 'all'.")

    print('-'*40)
    return city, month, day


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
