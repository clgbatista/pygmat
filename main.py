
import pandas as pd
import lib.pygmat as gmat

data = pd.read_csv('input/spire/satellite_coes_Spire.csv')

print(data)

for i in range(len(data)):
    spacecraft = gmat.SPACECRAFT()
    spacecraft.SMA = data["Semi-major axis (m)"][i]/1000
    spacecraft.ECC = data[" Eccentricity"][i]
    spacecraft.INC = data[" Inclination (rads)"][i]*360/2/3.14
    spacecraft.RAAN = data[" RAAN (rads)"][i]*360/2/3.14
    spacecraft.AOP = data[" Argument of Perigee (rads)"][i]*360/2/3.14
    spacecraft.TA = data[" Mean anomaly (rads)"][i]*360/2/3.14
    spacecraft.write_script(f'./00_sat_{i}_example.txt',name=f'sat{i}')


data = pd.read_csv('input/spire/groundstation_locations_Spire.csv')
for i in range(len(data)):
    groundStation = gmat.GROUND_STATION()
    groundStation.Location1 = data['Latitude (degs)'][i]
    groundStation.Location2 = data[' Longitude (degs)'][i]
    groundStation.write_script(f'./z40_gs_{i}_example.txt',name=f'gs{i}')

forceModel = gmat.FORCE_MODEL()
forceModel.write_script('./z50_fm_example.txt')

propagator = gmat.PROPAGATOR()
propagator.write_script('./z60_pr_example.txt')

eclipse = gmat.ECLIPSE_LOCATOR()
eclipse.Spacecraft = 'sat1'
eclipse.write_script('./z70_eclipse_example.txt',target_sat="sat1")

contact = gmat.CONTACT_LOCATOR()
contact.Observers = "{gs1, gs2}"
contact.Target = "sat1"
contact.Filename = "'sat1contact.txt'"
contact.write_script('./z80_contact_example.txt',target_sat="sat1")

gmat.mission_sequence(
    path_to_file="./z99_mission_sequence.txt",
    spacecrafts="sat0,sat1,sat2,sat3",
    ref_sat="sat0",
    time=10
)

gmat.write_script()

print(f'SUCCESS')