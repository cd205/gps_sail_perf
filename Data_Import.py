# %%
from typing import Dict, Union
from datetime import datetime
import gpxpy
import pandas as pd

class DataImport():
    _version ='1.0'

    @property
    def version(self):
        return type(self.version)
    
    
    def __init__(self) -> None:
        """ Initialise method, Schema and Column names
        """
        # The XML namespaces used by the GPX file for extensions, used when parsing the extensions
        self.NAMESPACES = {'garmin_tpe': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'}

        # The names of the columns we will use in our DataFrame
        self.COLUMN_NAMES = ['latitude', 'longitude', 'elevation', 'time', 'heart_rate', 'speed']
        return None

    
    def get_gpx_point_data(self, segment, pnt_num, point: gpxpy.gpx.GPXTrackPoint) -> Dict[str, Union[float, datetime, int]]:
            """Return a tuple containing some key data about `point`."""
            
            data = {
                'latitude': point.latitude,
                'longitude': point.longitude,
                'elevation': point.elevation,
                'time': point.time
            }
        
            # Parse extensions for heart rate and speed data, if available
            elem = point.extensions[0]  # Assuming we know there is only one extension
            try:
                data['heart_rate'] = int(elem.find('garmin_tpe:hr', self.NAMESPACES).text)
            except AttributeError:
                # "text" attribute not found, so data not available
                pass
                
            try:
                data['speed'] = segment.get_speed(pnt_num)
            except AttributeError:
                pass

            return data

    def get_dataframe_from_gpx(self, fname):# str) -> pd.DataFrame:
        """Takes the path to a GPX file (as a string) and returns a Pandas
        DataFrame.
        """
        with open(fname) as f:
            gpx = gpxpy.parse(f)
        segment = gpx.tracks[0].segments[0]  # Assuming we know that there is only one track and one segment
        data = [DataImport.get_gpx_point_data(self, segment, pnt_num, point) for pnt_num, point in enumerate(segment.points)]
        return pd.DataFrame(data, columns=self.COLUMN_NAMES)




if __name__ == '__main__':  
    from sys import argv
    #fname = argv[1]  # Path to GPX file to be given as first argument to script
    DataImporter = DataImport()
    df = DataImporter.get_dataframe_from_gpx(fname='rutland_13_05_2021.gpx')
    print(df)

    import folium   # (https://pypi.python.org/pypi/folium)
    mymap = folium.Map( location=[ df.latitude.mean(), df.longitude.mean() ], \
        zoom_start=14)
    folium.PolyLine(df[['latitude','longitude']].values, color="red", weight=2.5, opacity=1).add_to(mymap)
    #for coord in df[['latitude','longitude']].values:
    #    folium.CircleMarker(location=[coord[0],coord[1]], radius=1,
    #    color='red').add_to(mymap)
    # display(mymap)   # shows map inline in Jupyter but takes up full width
    #mymap.save('fol.html')  # saves to html file for display below





# %%
