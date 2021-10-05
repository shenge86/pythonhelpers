"""
QuickMaps Opener
@author: Shen Ge
@name: QuickMaps Opener
@description:
    Opens up quickmaps links based on your coordinates.
"""
import sys
import webbrowser
import pandas as pd

if __name__ == '__main__':
    try:
        inputfile = sys.argv[1]
        df = pd.read_csv(inputfile)
        print('Reading in csv file...')
        print('csv file must have two columns: 1 called lat and the other called lon')
    except:
        print('Could not find csv file.')
        print('Reading in default.')
        sys.exit(2)

    try:
        numrows = sys.argv[2]
    except:
        numrows = len(df) if len(df) < 100 else 100

    rows = df.index[0:numrows]

    print('Total # of points: ', numrows)
    linkcoords = ''
    for row in rows:
        lat = df['lat'][row]
        lon = df['lon'][row]
        print(row)
        print(f'Adding coordinate (lat, lon): {lat}, {lon}')
        linkcoords += f'{lon},{lat}|'

    botleftlon0 = df['lon'][0:numrows].min()-1
    botleftlat0 = df['lat'][0:numrows].min()-1
    toprightlon1 = df['lon'][0:numrows].max()+1
    toprightlat1 = df['lat'][0:numrows].max()+1

    # 16 is equidistant cylindrical plot
    link = f'https://quickmap.lroc.asu.edu/query?extent={botleftlon0},{botleftlat0},{toprightlon1},{toprightlat1}&proj=16&features='
    link+=linkcoords
    link = link[:-1]

    webbrowser.open(link,new=1)

    print('Finished opening QuickMaps.')
