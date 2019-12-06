import pandas as pd

from dao.basedao import BaseDAO
from utils import relative


def init_db(dao: BaseDAO):
    dao.connect_to_database()
    dao.drop_tables()
    dao.create_tables()
    dao.add_user("paj", "Paul", "Johnston", "123")
    user_names = ["paj"]
    dao.add_campus("Provo", "Utah", "BYU-Provo")
    dao.add_campus("Rexburg", "Idaho", "BYU-Idaho")
    dao.add_campus("Laie", "Hawaii", "BYU-Hawaii")
    dao.add_campus("SLC", "Utah", "BYU-SLC")
    campus_idProvo = dao.get_campus_id("BYU-Provo")
    campus_idRexburg = dao.get_campus_id("BYU-Idaho")
    campus_idLaie = dao.get_campus_id("BYU-Hawaii")
    campus_idSLC = dao.get_campus_id("BYU-SLC")
    building_names = []
    # Provo Campus
    myDF = pd.read_csv(
        relative(__file__, "Building_Coordinates.csv"),
        sep=",",
    )




    for i in range(0, len(myDF.index)):
        dao.add_building(
            myDF["Name"][i],
            float(myDF["Latitude"][i]),
            float(myDF["Longitude"][i]),
            campus_idProvo,
        )

        building_names.append(myDF["Name"][i])

    # Rexburg Campus
    myDF = pd.read_csv(
        relative(__file__, "Buildings_Rexburg.csv"),
        sep=",",
    )


    for i in range(0, len(myDF.index)):
        dao.add_building(
            myDF["Name"][i],
            float(myDF["Latitude"][i]),
            float(myDF["Longitude"][i]),
            campus_idRexburg,
        )

        building_names.append(myDF["Name"][i])

    # Laie Campus
    myDF = pd.read_csv(
        relative(__file__, "Buildings_Laie.csv"),
        sep=",",
    )

    for i in range(0, len(myDF.index)):
        dao.add_building(
            myDF["Name"][i],
            float(myDF["Latitude"][i]),
            float(myDF["Longitude"][i]),
            campus_idLaie,
        )

        building_names.append(myDF["Name"][i])


    # SLC Campus
    myDF = pd.read_csv(
        relative(__file__, "Buildings_SLC.csv"),
        sep=",",
    )

    for i in range(0, len(myDF.index)):
        dao.add_building(
            myDF["Name"][i],
            float(myDF["Latitude"][i]),
            float(myDF["Longitude"][i]),
            campus_idSLC,
        )

        building_names.append(myDF["Name"][i])


    # Fountains
    fountainData = pd.read_csv(
        relative(__file__, "FountainInput.csv"),
        sep=",",
    )

    fountain_names = []

    for i in range(0, len(fountainData.index)):
        building_idx = int(fountainData["Building_ID"][i]) - 1
        building_name = building_names[building_idx]
        building_id = dao.get_building_id(building_name)

        dao.add_fountain(
            building_id,
            str(fountainData["Fountain_Name"][i]),
        )

        fountain_names.append(fountainData["Fountain_Name"][i])

    ratingData = pd.read_csv(
        relative(__file__, "ratingInput.csv"),
        sep=",",
    )

    for i in range(0, len(ratingData.index)):
        fountain_idx = int(ratingData["Fountain_ID"][i]) - 1
        fountain_name = fountain_names[fountain_idx]
        fountain_id = dao.lookup_fountain(fountain_name)["id"]

        user_idx = int(ratingData["User_ID"][i]) - 1
        user_name = user_names[user_idx]
        user_id = dao.get_user_id(user_name)

        dao.add_rating(
            int(ratingData["Score"][i]),
            str(ratingData["Date"][i]),
            fountain_id,
            user_id,
        )

    dao.disconnect_from_database()
