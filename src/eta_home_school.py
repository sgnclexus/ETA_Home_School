import pandas as pd
import time
import sys
# from fuzzywuzzy import fuzz, process
# from rapidfuzz import fuzz, process
import Levenshtein

from utils.latitude_longitude import get_lat_long, get_travel_time
from utils.string_formatter import remove_accents, remove_after_cp

FINAL_COLS = [
    "FOLIO"
    ,"COLONIA"
    ,"CP"
    ,"ALCMUN_ASP"
    ,"EXPL_ASI"
    ,"NGLOBAL"
    ,"COPC_ASI"
    ,"NOPC_ASI"
    ,"PROMEDIO"
    ,"CVE_OPC"
    ,"NOM_ALCMUN"
    ,"INSTITU"
    ,"PLANTEL"
    ,"DOMICILIO"
    ,"NOM_CORTO"
    ,"Modo_Transporte"
    ,"Tiempo_en_Min"
    ,"Tiempo_Estimado_Arribo"
]


# Function to find best address match for a student based on the ZIP code
# def find_best_match(student_address, zip_code, sepomex_df):
#     # Filter SEPOMEX DataFrame by the student's zip code
#     sepomex_matches = sepomex_df[sepomex_df["d_codigo"] == zip_code]['d_asenta']
    
#     # Use fuzzy matching to find the best location match
#     best_match = process.extractOne(student_address, sepomex_matches, scorer=fuzz.ratio)
    
#     return best_match[0] if best_match else None

def find_best_match(student_address, zip_code, sepomex_df):
    """
    Function to find the best match in zip codes. SEPOMEX has the same zip code for multiple places, 
    so we use this function to select the more accuarate option based on student address
    """
    # Filter SEPOMEX locations by ZIP code
    sepomex_matches = sepomex_df[sepomex_df['d_codigo'] == zip_code]['d_asenta']
    
    # Initialize best match and best score
    best_match = None
    best_score = float('inf')  # The smaller the distance, the better
    
    # Loop through all SEPOMEX matches for the ZIP code
    for location in sepomex_matches:
        # Calculate the Levenshtein distance between the addresses
        score = Levenshtein.distance(student_address, location)
        
        # If the new score is better (smaller), update the best match
        if score < best_score:
            best_score = score
            best_match = location
    
    return best_match


def get_eta(dfOriginDestination):
    """
    function that receives a dataframe with column ORIGEN and DESTINO to get the elapsed time arrival
    """

    try:
        # Step 4: Filter the top 5 rows within each group
        dfOriginDestination[["Tiempo_en_Min", "Tiempo_Estimado_Arribo","Modo_Transporte"]] = dfOriginDestination.apply(lambda row: pd.Series(get_travel_time(row["ORIGEN"],row["DESTINO"])), axis=1)
        dfOriginDestination.to_csv("Asignado_Casa_Escuela_Tiempo_Estimado_Arribo.csv", sep=",", encoding="utf-8", mode="w", index=False)
        print("API Direction succeful result")
        

        """
        We found some cases where location is not possible by "transit" mode, so in this cases we execute by "driving" mode 
        and recover the mode to print in the excel
        """
        dfNotByTransit = dfOriginDestination[dfOriginDestination["Modo_Transporte"].isna()].copy()        

        if len(dfNotByTransit) > 0:
            dfNotByTransit[["Tiempo_en_Min", "Tiempo_Estimado_Arribo","Modo_Transporte"]] = dfNotByTransit.apply(lambda row: pd.Series(get_travel_time(row["ORIGEN"],row["DESTINO"], "driving")), axis=1)
            dfByTransit = dfOriginDestination[dfOriginDestination["Modo_Transporte"].notna()].copy()
            return pd.concat([dfByTransit, dfNotByTransit])
        else: 
            return dfOriginDestination       

            
    
    except:
        print("API Error")
        return None


def execution_proccess(since_question):
    """
    Function to prepare and proccess information to get elapsed time arrival to assigned school
    This function consider:
    -SEPOMEX information 
    -Latitutde Longitude of all schools (Note, in some cases we didn't find the exact location, so we find manually)    
    """

    try:        
        
        # Get data from Schools
        dfSchool = pd.read_csv("data\OpcEdu.csv", sep="|", encoding="utf-8")    
        dfSchoolReqCols = dfSchool[["CVE_OPC","NOM_ALCMUN","INSTITU","PLANTEL","DOMICILIO","NOM_CORTO"]]
        dfSchoolReqCols.to_csv("ScholsRequiredCols.csv",sep="|", encoding="utf-8", index=False)
        print("Schools with required columns created")
        
        """
        Adding column with function remove_after_cp applied. 
        We use regular expression to delete phone(s) and email(s)
        """
        # Safe copy of the DataFrame to avoid warnings
        dfSchoolReqCols = dfSchoolReqCols.copy()
        dfSchoolReqCols.loc[:,"DOMICILIO_MOD"] = dfSchoolReqCols["DOMICILIO"].str.upper().apply(remove_after_cp)
        dfSchoolReqCols["PLANTEL"] = dfSchoolReqCols["PLANTEL"].str.strip()
        dfSchoolReqCols.to_csv("ScholsRemovingAfter_CP.csv",sep="|", encoding="utf-8", index=False)
        print("Schools with required columns and removing unnecesary data created")
        
        """
        Grouping data based on new column "DOMICILIO_MOD"
        """
        dfUniqueSchool = pd.DataFrame(dfSchoolReqCols["DOMICILIO_MOD"].unique(), columns=["UNIQUE_ADDRESS"])
        dfUniqueSchool.to_csv("UniqueSchools.csv", sep="|", encoding="utf-8", index=False)                
        print("Schools Group By function to get unique schools created")

        # dfUunique_School_Address = dfSchoolReqCols[["PLANTEL","DOMICILIO_MOD"]].drop_duplicates()    
        # dfUniqueSchool.to_csv("UniqueSchoolsAddress.csv", sep="|", encoding="utf-8")
        # dfUniqueSchool.to_csv("UniqueSchools.csv", sep=",", encoding="utf-8")

        # """
        # We use google maps api to find latitude and longitude considering name of the school and address of the school, both cases
        # """
        # dfUniqueSchool[["LatitudeAdd","LongitudeAdd"]] = dfUniqueSchool.apply(lambda row: pd.Series(get_lat_long(row["UNIQUE_ADDRESS"])), axis=1)
        # dfUunique_School_Address[["LatitudeName","LongitudeName"]] = dfUunique_School_Address.apply(lambda row: pd.Series(get_lat_long(row["PLANTEL"])), axis=1)    

        # Some testing
        # dfUunique_School_Address.to_csv("UniqueSchools3.csv", sep=",", encoding="utf-8", index=False)
        # dfLatLong = pd.read_csv("ValidaciionLatitudLongitud_BKP.csv", sep="|", encoding="utf-8")
        # paValidar = pd.merge(dfUunique_School_Address,dfLatLong, how="inner", left_on="DOMICILIO_MOD", right_on="UNIQUE_ADDRESS")
        # paValidar.to_csv("ValidaciionLatitudLongitud.csv", sep="|", encoding="utf-8")


        """
        We now read the final approach of Latitude Longitude of COMIPEMS schools
        The idea it to join with the opc_edu to ensure the exact precision of each school.
        """
        dfLatLogFinal = pd.read_csv("data\ETA_Schools_Final_LatitudeLongitude.csv", sep=",", encoding="utf-8")
        # Merge with original file
        dfLatLogFinal["PLANTEL"] = dfLatLogFinal["PLANTEL"].str.strip()
        dfFinalOpcEdu = pd.merge(dfSchoolReqCols, dfLatLogFinal, how="left", left_on="PLANTEL", right_on="PLANTEL", suffixes=["","_"])
        dfFinalOpcEdu.to_csv("FinalOpcEdu.csv",sep="|", encoding="utf-8", index=False)
        print("Schools merged with final latitude longitude file created")


        """
        Now we are going to get students from final file obtained of assignement process
        """
        columns_to_load = ["FOLIO","COLONIA","CP","ALCMUN_ASP","EXPL_ASI","NO_PRES","NGLOBAL","COPC_ASI","NOPC_ASI","PROMEDIO","OPC_ED01"]
        dfAssignedDS = pd.read_csv("data\Metro_2024_global.csv", sep="|", encoding="utf-8", dtype={"FOLIO":str, "CP":str}, low_memory=False, usecols=columns_to_load)    
        # print("Metro into dataframe")
        #dfAssignedDS["ORIGEN"] = dfAssignedDS["CP"] + " " + dfAssignedDS["ALCMUN_ASP"] + " " + dfAssignedDS["COLONIA"] # va antes la colonia  colinia alcadia/municipio ciudad y estado separado por comas 

        """
        We apply some filters to get a section of all universe of students
        """
        f1 = dfAssignedDS["EXPL_ASI"] == "ASI"
        f2 = dfAssignedDS["NO_PRES"] == "SP"
        f3 = dfAssignedDS["NGLOBAL"] >= int(since_question)
        f4 = dfAssignedDS["ALCMUN_ASP"] != "EXTRANJERO"       # We added because address in foreign people ocasionally is blank    
        dfAssigned = dfAssignedDS[f1 & f2  & f3 & f4]
        dfAssigned.to_csv("Assigned_Filtered.csv", sep="|", encoding="utf-8")
        print("Assigned Students File created")

        """
        Now we recover info of SEPOMEX (Approach to get the right locations)
        After that we merge info with Assigned students file
        """
        dfsepomex = pd.read_csv("data\CPdescarga.csv", sep="|", encoding="utf-8", low_memory=False, dtype={"d_codigo":str})
        dfsepomex["d_asenta"] = dfsepomex["d_asenta"].str.upper().apply(remove_accents)        
        #dfAssignedRigthAddress = pd.merge(dfAssigned, dfsepomex, how="inner", left_on=["CP","COLONIA"], right_on=["d_codigo","d_asenta"])    
        #dfAssignedRigthAddress = pd.merge(dfAssigned, dfsepomex, how="inner", left_on=["CP"], right_on=["d_codigo"])    
        dfAssignedRigthAddress = dfAssigned.copy()
        dfAssignedRigthAddress["BEST_ASENTA"] = dfAssignedRigthAddress.apply(lambda row: find_best_match(row["COLONIA"],row["CP"], dfsepomex), axis=1)
        dfAssignedRigthAddress.to_csv("AssignedSEPOMEX.csv", sep="|", encoding="utf-8", index=False)
        print("Merged info between SEPOMEX and Assigned Students file created")

        """
        After we associate the best approach to each student we merge to sepomex to get all info from sepomex
        We are going to use this info to create the origin field 
        """
        dfFinalSepomex = pd.merge(dfAssignedRigthAddress,dfsepomex, how="inner", left_on=["CP","BEST_ASENTA"], right_on=["d_codigo","d_asenta"])

        """
        Now we have all info in one dataframe we start final phase, we get the final origin field and destination field        
        """
        dfAssignedSchool = pd.merge(dfFinalSepomex, dfFinalOpcEdu, how="inner", left_on="COPC_ASI", right_on="CVE_OPC", suffixes=["","_"])
        dfAssignedSchool["ORIGEN"] = dfAssignedSchool["d_asenta"].fillna('').str.strip() + "," + dfAssignedSchool["D_mnpio"].fillna('').str.strip() + "," + dfAssignedSchool["d_ciudad"].fillna('').str.strip() + "," +  dfAssignedSchool["d_codigo"].fillna('').str.strip()
        dfAssignedSchool["KEY_ETA"] = dfAssignedSchool["d_asenta"].fillna('').str.strip() + "_" + dfAssignedSchool["D_mnpio"].fillna('').str.strip() + "_" + dfAssignedSchool["d_ciudad"].fillna('').str.strip() + "_" + dfAssignedSchool["d_codigo"].fillna('').str.strip() + "_" + dfAssignedSchool["Latitud-Longitud Final"].fillna('').str.strip() 
        dfAssignedSchool.to_csv("AllInfoforETA.csv", sep="|", encoding="utf-8", index=False)    
        print("All info in one file created")

        # """
        # For testing purpose
        # """
        # dfETAtoSend = pd.DataFrame(dfAssignedSchool["KEY_ETA"].unique(), columns=["KEY_ETA"])    
        # dfETAtoSend.to_csv("Unique_ETAs.csv")

        """
        After we create origin field, we group that information based on the next 3 values:
        -ORIGEN
        -Latitud_Final
        -Longitud_Final
        We are going to use it as a key to find concurrancy between students living in similar locations and was assigned to the same school
        The purpose is to avoid unnecessary requests to the api
        """
        # dfGetETA = dfAssignedSchool.groupby(["ORIGEN","Latitud_final","Longitud_final"]).sum().reset_index()
        dfGetETA = dfAssignedSchool.groupby(["ORIGEN","Latitud_final","Longitud_final", "KEY_ETA"]).count().reset_index()
        dfGetETA["DESTINO"] = dfGetETA["Latitud_final"].astype(str).str.strip() + "," + dfGetETA["Longitud_final"].astype(str).str.strip()
        dfGetETA.to_csv("FinalFileToETA.csv", sep="|", encoding="utf-8", index=False)
        print("Final file to request api direction created")

        dfETA = get_eta(dfGetETA)

        """
        Finally we merge again with All info in one file to apply to all occurrences the elapsed time arrival

        """
        if len(dfETA) > 0:
            dfETA_Assigned = pd.merge(dfAssignedSchool, dfETA, how="inner", right_on=["KEY_ETA"], left_on=["KEY_ETA"], suffixes=["","_"])
            dfETA_Assigned = dfETA_Assigned[FINAL_COLS]
            dfETA_Assigned.to_excel("OA_Trayecto_Casa_Escuela.xlsx", index=False)
            print("Final File to analysis created")


        return True
    
    except Exception as ex:
        print("Error : ", ex)
        return False
    
def po_execution_proccess(since_question):
    """
    Function to prepare and proccess information to get elapsed time arrival to the first option chossed
    This function consider:
    -SEPOMEX information 
    -Latitutde Longitude of all schools (Note, in some cases we didn't find the exact location, so we find manually)    
    """

    try:        
        
        # Get data from Schools
        dfSchool = pd.read_csv("data\OpcEdu.csv", sep="|", encoding="utf-8")    
        dfSchoolReqCols = dfSchool[["CVE_OPC","NOM_ALCMUN","INSTITU","PLANTEL","DOMICILIO","NOM_CORTO"]]
        dfSchoolReqCols.to_csv("ScholsRequiredCols.csv",sep="|", encoding="utf-8", index=False)
        print("Schools with required columns created")
        
        """
        Adding column with function remove_after_cp applied. 
        We use regular expression to delete phone(s) and email(s)
        """
        # Safe copy of the DataFrame to avoid warnings
        dfSchoolReqCols = dfSchoolReqCols.copy()
        dfSchoolReqCols.loc[:,"DOMICILIO_MOD"] = dfSchoolReqCols["DOMICILIO"].str.upper().apply(remove_after_cp)
        dfSchoolReqCols["PLANTEL"] = dfSchoolReqCols["PLANTEL"].str.strip()
        dfSchoolReqCols.to_csv("ScholsRemovingAfter_CP.csv",sep="|", encoding="utf-8", index=False)
        print("Schools with required columns and removing unnecesary data created")
        
        """
        Grouping data based on new column "DOMICILIO_MOD"
        """
        dfUniqueSchool = pd.DataFrame(dfSchoolReqCols["DOMICILIO_MOD"].unique(), columns=["UNIQUE_ADDRESS"])
        dfUniqueSchool.to_csv("UniqueSchools.csv", sep="|", encoding="utf-8", index=False)                
        print("Schools Group By function to get unique schools created")

        """
        We now read the final approach of Latitude Longitude of COMIPEMS schools
        The idea it to join with the opc_edu to ensure the exact precision of each school.
        """
        dfLatLogFinal = pd.read_csv("data\ETA_Schools_Final_LatitudeLongitude.csv", sep=",", encoding="utf-8")
        # Merge with original file
        dfLatLogFinal["PLANTEL"] = dfLatLogFinal["PLANTEL"].str.strip()
        dfFinalOpcEdu = pd.merge(dfSchoolReqCols, dfLatLogFinal, how="left", left_on="PLANTEL", right_on="PLANTEL", suffixes=["","_"])
        dfFinalOpcEdu.to_csv("FinalOpcEdu.csv",sep="|", encoding="utf-8", index=False)
        print("Schools merged with final latitude longitude file created")


        """
        Now we are going to get students from final file obtained of assignement process
        """
        columns_to_load = ["FOLIO","COLONIA","CP","ALCMUN_ASP","EXPL_ASI","NO_PRES","NGLOBAL","COPC_ASI","NOPC_ASI","PROMEDIO","OPC_ED01"]
        dfAssignedDS = pd.read_csv("data\Metro_2024_global.csv", sep="|", encoding="utf-8", dtype={"FOLIO":str, "CP":str}, low_memory=False, usecols=columns_to_load)    

        """
        We apply some filters to get a section of all universe of students
        """
        # f1 = dfAssignedDS["EXPL_ASI"] == "ASI"
        f2 = dfAssignedDS["NO_PRES"] == "SP"
        f3 = dfAssignedDS["NGLOBAL"] >= int(since_question)
        f4 = dfAssignedDS["ALCMUN_ASP"] != "EXTRANJERO"       # We added because address in foreign people ocasionally is blank    
        dfAssigned = dfAssignedDS[f2  & f3 & f4]
        dfAssigned.to_csv("Assigned_Filtered.csv", sep="|", encoding="utf-8")
        print("Assigned Students File created")

        """
        Now we recover info of SEPOMEX (Approach to get the right locations)
        After that we merge info with Assigned students file
        """
        dfsepomex = pd.read_csv("data\CPdescarga.csv", sep="|", encoding="utf-8", low_memory=False, dtype={"d_codigo":str})
        dfsepomex["d_asenta"] = dfsepomex["d_asenta"].str.upper().apply(remove_accents)        
        #dfAssignedRigthAddress = pd.merge(dfAssigned, dfsepomex, how="inner", left_on=["CP","COLONIA"], right_on=["d_codigo","d_asenta"])    
        #dfAssignedRigthAddress = pd.merge(dfAssigned, dfsepomex, how="inner", left_on=["CP"], right_on=["d_codigo"])    
        dfAssignedRigthAddress = dfAssigned.copy()
        dfAssignedRigthAddress["BEST_ASENTA"] = dfAssignedRigthAddress.apply(lambda row: find_best_match(row["COLONIA"],row["CP"], dfsepomex), axis=1)
        dfAssignedRigthAddress.to_csv("AssignedSEPOMEX.csv", sep="|", encoding="utf-8", index=False)
        print("Merged info between SEPOMEX and Assigned Students file created")

        """
        After we associate the best approach to each student we merge to sepomex to get all info from sepomex
        We are going to use this info to create the origin field 
        """
        dfFinalSepomex = pd.merge(dfAssignedRigthAddress,dfsepomex, how="inner", left_on=["CP","BEST_ASENTA"], right_on=["d_codigo","d_asenta"])

        """
        Now we have all info in one dataframe we start final phase, we get the final origin field and destination field        
        We merge information base on the first option the student choose
        """
        dfAssignedSchool = pd.merge(dfFinalSepomex, dfFinalOpcEdu, how="inner", left_on="OPC_ED01", right_on="CVE_OPC", suffixes=["","_"])
        dfAssignedSchool["ORIGEN"] = dfAssignedSchool["d_asenta"].fillna('').str.strip() + "," + dfAssignedSchool["D_mnpio"].fillna('').str.strip() + "," + dfAssignedSchool["d_ciudad"].fillna('').str.strip() + "," +  dfAssignedSchool["d_codigo"].fillna('').str.strip()
        dfAssignedSchool["KEY_ETA"] = dfAssignedSchool["d_asenta"].fillna('').str.strip() + "_" + dfAssignedSchool["D_mnpio"].fillna('').str.strip() + "_" + dfAssignedSchool["d_ciudad"].fillna('').str.strip() + "_" + dfAssignedSchool["d_codigo"].fillna('').str.strip() + "_" + dfAssignedSchool["Latitud-Longitud Final"].fillna('').str.strip() 
        dfAssignedSchool.to_csv("AllInfoforETA.csv", sep="|", encoding="utf-8", index=False)    
        print("All info in one file created")

        # """
        # For testing purpose
        # """
        # dfETAtoSend = pd.DataFrame(dfAssignedSchool["KEY_ETA"].unique(), columns=["KEY_ETA"])    
        # dfETAtoSend.to_csv("Unique_ETAs.csv")

        """
        After we create origin field, we group that information based on the next 3 values:
        -ORIGEN
        -Latitud_Final
        -Longitud_Final
        We are going to use it as a key to find concurrancy between students living in similar locations and was assigned to the same school
        The purpose is to avoid unnecessary requests to the api
        """
        dfGetETA = dfAssignedSchool.groupby(["ORIGEN","Latitud_final","Longitud_final", "KEY_ETA"]).count().reset_index()
        dfGetETA["DESTINO"] = dfGetETA["Latitud_final"].astype(str).str.strip() + "," + dfGetETA["Longitud_final"].astype(str).str.strip()
        dfGetETA.to_csv("FinalFileToETA.csv", sep="|", encoding="utf-8", index=False)
        print("Final file to request api direction created")

        dfETA = get_eta(dfGetETA)

        """
        Finally we merge again with All info in one file to apply to all occurrences the elapsed time arrival

        """
        if len(dfETA) > 0:
            dfETA_Assigned = pd.merge(dfAssignedSchool, dfETA, how="inner", right_on=["KEY_ETA"], left_on=["KEY_ETA"], suffixes=["","_"])
            dfETA_Assigned = dfETA_Assigned[FINAL_COLS]
            dfETA_Assigned.to_excel("PO_Trayecto_Casa_Escuela.xlsx", index=False)
            print("Final File to analysis created")


        return True
    
    except Exception as ex:
        print("Error : ", ex)
        return False    

def result_generation(file_operation, since_question=120):
    """
    Menu Options 
    """
    if file_operation == "-oa":
        if execution_proccess(since_question):
            print("ETA finished without errors")
        else:
            print("Error in execution")
    elif file_operation == "-po":
        if po_execution_proccess(since_question):
            print("ETA finished without errors")
        else:
            print("Error in execution")
    else:
        print("Opcion no valida")
        instructions()
        return


def instructions():
    print("---------------------------------------------------------------------------------")
    print("Para realizar la ejecución, el script requiere dos argumentos")
    print("El primer argumento permite indicar si se genera el archivo")
    print("en base a la opción asignada o en base a la 1ra opción que coloco el sustentante")
    print("\t* -oa para generar el archivo por la opción asignada")
    print("\t* -po para generar el archivo por la primer opcion elegida")
    print("El segundo argumento le indica a partir de que reactivo empieza va a filtrar")
    print("los datos en forma descendente, se puede omitir con un default de 125")
    print("\t* [1-128] Son los valores permitidos")
    print("El producto final es un excel llamado Trayecto_Casa_Escuela.xlsx")
    print("---------------------------------------------------------------------------------")

# print(df)
if __name__ == '__main__':
    
    arguments = sys.argv

    # """
    # """

    # # Creating the dataframe
    # df = pd.read_csv("data//nba.csv")

    # # Print the dataframe
    # print(df.head())

    # # applying groupby() function to
    # # group the data on team value.
    # gk = df.groupby(['Team','Position']).count().reset_index()

    # # Let's print the first entries
    # # in all the groups formed.
    # pd = pd.DataFrame(gk)
    # print(pd)

    # """
    # """


    start_time = time.strftime("%H:%M:%S", time.localtime())    
    print("Begin Task : ", start_time)

    if len(arguments) == 2:
        result_generation(arguments[1])
    elif len(arguments) == 3:
        result_generation(arguments[1],arguments[2])
    else:
        instructions()
    
    end_time = time.strftime("%H:%M:%S", time.localtime())
    print("End Task : ", end_time)

