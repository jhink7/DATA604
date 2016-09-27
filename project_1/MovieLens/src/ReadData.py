'''
Created on Jun 8, 2012

@author: yyb
'''

#'Read user information from users.dat, movie information from movies.dat, rating information from ratings.dat'

from datetime import datetime;

usrDict = {};  # a dictionary for storing UserIDs and their corresponding properties
movDict = {};  # a dictionary for storing MovieIDs and their corresponding properties
dateDict = {};  # a dictionary for storing dates(year-mon-day) and corresponding ratings (UserIDs, MovieIDs)
monDict = {};  # a dictionary for storing months(year-mon) and corresponding ratings (UserIDs, MovieIDs)
yearDict = {};  # a dictionary for storing years(year) and corresponding ratings (UserIDs, MovieIDs)
ratDict = {};  # a dictionary for storing (UserID,MovieID) and its corresponding rating value and timestamp

dateList = [];  # a list for storing all the dates of ratings
monList = [];  # a list for storing all the months of ratings
yearList = [];  # a list for storing all the years of ratings


# ===============================================================================
# Read information of users: UserID, Gender, Age, Occupation, Zipcode
# ===============================================================================
def readUserInfo():
    fobj = open('../Raw Data/users.dat', 'r');
    while True:
        s = fobj.readline();
        if len(s) == 0:
            break;
        [uid, gender, age, occup, zcode] = s.split('::');
        uid = 'U' + uid;
        age = get_age(age);
        zcode = zcode.strip();
        occup = get_occupation(occup);
        usrDict[uid] = [(gender, age, occup, zcode), 0];

    fobj.close();


# ===============================================================================
# Get information about age
# ===============================================================================
def get_age(age):
    if age == '1':
        return 'Under 18';
    elif age == '18':
        return '18-24';
    elif age == '25':
        return '25-34';
    elif age == '35':
        return '35-44';
    elif age == '45':
        return '45-49';
    elif age == '50':
        return '50-55';
    elif age == '56':
        return '56+';
    else:
        return 'None';


# ===============================================================================
# Get information about occupation
# ===============================================================================
def get_occupation(occup):
    if occup == '0':
        return 'other or not specified';
    elif occup == '1':
        return 'academic/educator';
    elif occup == '2':
        return 'artist';
    elif occup == '3':
        return 'clerical/admin';
    elif occup == '4':
        return 'college/grad student';
    elif occup == '5':
        return 'customer service';
    elif occup == '6':
        return 'doctor/health care';
    elif occup == '7':
        return 'executive/managerial';
    elif occup == '8':
        return 'farmer';
    elif occup == '9':
        return 'homemaker';
    elif occup == '10':
        return 'K-12 student';
    elif occup == '11':
        return 'lawyer';
    elif occup == '12':
        return 'programmer';
    elif occup == '13':
        return 'retired';
    elif occup == '14':
        return 'sales/marketing';
    elif occup == '15':
        return 'scientist';
    elif occup == '16':
        return 'self-employed';
    elif occup == '17':
        return 'technician/engineer';
    elif occup == '18':
        return 'tradesman/craftsman';
    elif occup == '19':
        return 'unemployed';
    elif occup == '20':
        return 'writer';
    else:
        return 'other or not specified';


# ===============================================================================
# Read information of movies: MovieID, Title, Genres
# ===============================================================================
def readMovieInfo():
    fobj = open('../Raw Data/outmovies.dat', 'r');
    while True:
        s = fobj.readline();
        if len(s) == 0:
            break;
        [mid, title, genres] = s.split('::');
        mid = 'M' + mid;
        genres = genres.strip();
        movDict[mid] = [(title, genres), 0];

    fobj.close();


# ===============================================================================
# Read information about ratings: UserID, MovieID, rating, timestamp
# ===============================================================================
def readRatingInfo():
    fobj = open('../Raw Data/ratings.dat', 'r');
    while True:
        s = fobj.readline();
        if len(s) == 0:
            break;
        [uid, mid, rate, tmstmp] = s.split('::');
        uid = 'U' + uid;
        mid = 'M' + mid;
        rate = int(rate);
        tmstmp = int(tmstmp);
        tmstmp = datetime.utcfromtimestamp(tmstmp);
        tmstmp = tmstmp.isoformat(' ');
        ratDict[(uid, mid)] = (rate, tmstmp);
        yr = tmstmp[0:4];
        mon = tmstmp[0:7];
        day = tmstmp[0:10];
        if yr in yearDict:
            yearDict[yr].append((uid, mid));
        else:
            yearDict[yr] = [(uid, mid)];
            yearList.append(yr);
        if mon in monDict:
            monDict[mon].append((uid, mid));
        else:
            monDict[mon] = [(uid, mid)];
            monList.append(mon);
        if day in dateDict:
            dateDict[day].append((uid, mid));
        else:
            dateDict[day] = [(uid, mid)];
            dateList.append(day);

        yearList.sort();
        monList.sort();
        dateList.sort();

