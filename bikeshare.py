import time
import pandas as pd
import numpy as np
import datetime as dt
from IPython.display import display
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6}

date_type=""

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
    
    city=""
    valid_city = False
    print("Would you like to see data for Chicago, New York or Washington?")
    while valid_city == False:
        city = input()
        if city in ("Chicago","New York","Washington"):
            valid_city = True
        else:
            print('-'*40)
            print("Invalid city! Type Chicago, New York or Washington")
            print('-'*40)

    # TO DO: get user input for month (all, january, february, ... , june)
    print("")
    print("Would you like to data by month, day, both or not at all? Type \"none\" for no time filter.")
    global date_type
    while date_type not in ("month","day","both","none"):
        date_type = input()
        if date_type not in ("month","day","both","none"):
            print('-'*40)
            print("Invalid Type! Type month,day,both or none")
            print('-'*40)
    
    month=""        
    if date_type in ("month","both"):
        print("")
        print("Which month? January, February, March, April, May or June")
        while month not in ("January", "February", "March", "April", "May", "June"):
            month = input()
            if month not in ("January", "February", "March", "April", "May", "June"):
                print('-'*40)
                print("Invalid month! Type January, February, March, April, May or June")
                print('-'*40)
        
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = 0
    if date_type in ("day","both"):
        print("")
        print("Which day? Please type your response as an integer (a.g., 1=Sunday).")
        valid_day = False
        while valid_day == False:
            try:
                day = int(input ())
                if day > 0 and day < 8:
                    valid_day=True
                else:
                    print('-'*40)
                    print("Invalid day! Type your response as an integer between 1 and 7")
                    print('-'*40)
            except:
                print('-'*40)
                print("Invalid day! Type your response as an integer")
                print('-'*40)

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
    if city == "New York":
        city = "New York City"
    df = pd.read_csv("./"+CITY_DATA[city.lower()]) 
    """if city =="Chicago":
        df = pd.read_csv("./chicago.csv")
    elif city =="New York":
        df = pd.read_csv("./new_york_city.csv")
    else :
        df = pd.read_csv("./washington.csv")
    """
    format = '%b %d %Y %I:%M%p' # The format 
    df['Start Time']= pd.to_datetime(df['Start Time']) 
    df['End Time']= pd.to_datetime(df['End Time']) 
    
    
    if month != "":
        df = df[df['Start Time'].dt.month==MONTH_DATA[month]]
    
    
    if day !=0:
        df = df[df['Start Time'].dt.dayofweek==((day+5)%7)]
    
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['Start Time'] = pd.to_datetime(df["Start Time"])


    # TO DO: display the most common day of week
    df['dayofweek'] = df["Start Time"].dt.dayofweek
    dayofweek = df['dayofweek'].mode()[0]
    
    
    # TO DO: display the most common start hour
    df['hour'] = df["Start Time"].dt.hour
    start_hour = df['hour'].mode()[0]
    
    df2 = df[df['Start Time'].dt.hour==start_hour] 
    
    print("Most popular day:{}".format(dayofweek))
    print("Most popular hour:{}".format(start_hour))
    print("Count:{}".format(df2["Start Time"].count()))
    print("Filter:{}".format(date_type))  
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("start_station:{}".format(start_station))
    df3 = df[df['Start Station']==start_station] 
    print("Count:{}".format(df3['Start Station'].count()))
    
    # TO DO: display most commonly used end station
    end_station = df["End Station"].mode()[0]
    print("end_station:{}".format(end_station))
    df4 = df[df['End Station']==end_station] 
    print("Count:{}".format(df4['End Station'].count()))
    
    # TO DO: display most frequent combination of start station and end station trip
    
    counts = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print("Trip :{}".format(counts.index[0]))
    print("Count : {}".format(counts[0]))
    print("Filter:{}".format(date_type))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    
    print("Total duration:{}".format(df["Trip Duration"].sum()))
    print("Count:{}".format(df['Trip Duration'].count()))

    # TO DO: display mean travel time
    print("Avg duration:{}".format(df["Trip Duration"].mean()))
    print("Filter:{}".format(date_type))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    
    counts = df.groupby(['User Type']).size().sort_values(ascending=False)
    
    
    
    for i in range(len(counts)) : 
        print("{}:{}".format(counts.index[i],counts[i]))
    print("Filter:{}".format(date_type))    
    
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        counts = df.groupby(['Gender']).size().sort_values(ascending=False)
        for i in range(len(counts)) : 
            print("{}:{}".format(counts.index[i],counts[i]))
    else:
        print("No gender data to share.")
    print("Filter:{}".format(date_type))
    # TO DO: Display earliest, most recent, and most common year of birth
    
    """df["Birth Year"]= pd.to_datetime(df["Birth Year"]) """
    if 'Birth Year' in df.columns:
        print("Earliest year of birth:{}".format(df["Birth Year"].min()))
        print("Most recent year of birth:{}".format(df["Birth Year"].max()))
        print("Most common year of birth:{}".format(df["Birth Year"].mode()[0]))
    else:
        print("No birth year data to share.")
    print("Filter:{}".format(date_type))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        counter=0
        while True:
            df_json = df.iloc[counter:(counter+5)].to_json(orient='records')
            formatted_json = json.dumps(json.loads(df_json), indent=4)
            print(formatted_json)
            counter+=5
            
            show_more = input("\nWould you like to view individual trip data?Type \'yes\' or \'no\'. \n")
            if show_more.lower()!='yes':
                break
            
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

