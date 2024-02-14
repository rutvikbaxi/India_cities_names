import pandas as pd
import plotly.express as px

df = pd.read_csv("pincode.csv")
mapbox_token = "pk.eyJ1IjoicnV0dmlrZGVsaGl2ZXJ5IiwiYSI6ImNscGkzZDV6djBjajUyaXFxdnpyaDJqa3YifQ.e-hd9gQUo6l0ObHwAoUk2A"

df = df[["District", "Latitude", "Longitude"]].reset_index(drop=True)
df.dropna(inplace=True)

def try_float_conversion(value):
    try:
        return float(value)
    except ValueError:
        return None
    
df["Latitude"] = df["Latitude"].astype(str)
df["Latitude"] = df["Latitude"].apply(try_float_conversion)

df["Longitude"] = df["Longitude"].astype(str)
df["Longitude"] = df["Longitude"].apply(try_float_conversion)

df_coords = df.groupby('District').agg({"Latitude" : 'median', "Longitude" : 'median'}).reset_index()

df_coords["ends_with"] = None
df_coords.loc[df_coords.District.str.upper().str.endswith('PUR'), "ends_with"] = "pur"
df_coords.loc[df_coords.District.str.upper().str.endswith('PURAM'), "ends_with"] = "puram"

df_coords.dropna(inplace=True)

px.set_mapbox_access_token(mapbox_token)
fig = px.scatter_mapbox(df_coords, lat="Latitude", lon="Longitude", hover_name="District", color="ends_with",
                        mapbox_style="basic", zoom=4)

fig.show()