import os
import string
import random
from flask import abort, Flask, jsonify, request

ERRORMSG = "You address format was incorrect, please make sure it is correct. IE: 123 XXX ST"

ADDYSHORTCUT = [
                ["ALLEY","ALLEE","ALY","ALLEY", "ALLY","ALY"],
                ["ANEX","ANEX","ANX,""ANNEX","ANNX","ANX"],
                ["ARCADE","ARC","ARC","ARCADE"],
                ["AV","AVE","AVEN","AVENU","AVENUE","AVN","AVNUE"],
                ["BAYOU","BAYOO","BYU","BAYOU"],
                ["BEACH","BCH","BCH","BEACH"],
                ["BEND","BEND","BND","BND"],
                ["BLUFF","BLF","BLUF"],
                ["BLUFFS","BLUFFS","BLFS"],
                ["BOTTOM","BOT","BTM","BOTTM"],
                ["BOULEVARD","BLVD","BLVD","BOUL","BOULV"],
                ["BRANCH","BR","BRNCH"],
                ["BRIDGE","BRDGE","BRG"],
                ["BROOK","BRK"],
                ["BROOKS","BRKS"],
                ["BURG","BG"],
                ["BURGS","BGS"],
                ["BYP","BYPA","BYPAS","BYPASS","BYPS"],
                ["CAMP","CP","CMP"],
                ["CANYN","CYN","CANYON","CNYN"],
                ["CAPE","CPE"],
                ["CAUSEWAY","CSWY","CAUSWA","CSWY"],
                ["CENTER","CEN","CENT","CENTER","CENTR","CENTRE","CNTR","CTR"],
                ["CENTERS","CTRS"],
                ["CIRCLE","CIR","CIRC","CIRCL","CRCL","CRCLE"],
                ["CIRCLES","CIRS"],
                ["CLIFF","CLF"],
                ["CLIFFS","CLFS"],
                ["CLB","CLUB"],
                ["COMMON","CMN"],
                ["COMMONS""CMNS"],
                ["CORNER","COR"],
                ["CORNERS","CORS"],
                ["COURSE","CRSE"],
                ["COURT","CT"],
                ["COURTS","CTS"],
                ["COVE","CV"],
                ["COVES","CVS"],
                ["CREEK","CRK"],
                ["CRESCENT","CRES"],
                ["CRSENT","CRSNT","CREST","CRST"],
                ["CROSSING","XING","CRSSNG"],
                ["CROSSROAD","XRD"],
                ["CROSSROADS","XRDS"],
                ["CURVE","CURV"],
                ["DALE","DL"],
                ["DAM","DM"],
                ["DIVIDE","DIV","DV","DVD"],
                ["DRIVE","DR","DRIV","DRV"],
                ["DRIVES","DRS"],
                ["ESTATE","EST"],
                ["ESTATES","ESTS"],
                ["EXPRESSWAY","EXP","EXPY","EXPR","EXPRESS","EXPW"],
                ["EXTENSION","EXT","EXTN","EXTNSN"],
                ["EXTENSIONS","EXTS"],
                ["FALL"],
                ["FALLS","FLS"],
                ["FERRY","FRY","FRRY"],
                ["FIELD","FLD"],
                ["FIELDS","FLDS"],
                ["FLAT","FLT"],
                ["FLATS","FLTS"],
                ["FORD","FRD"],
                ["FORDS","FRDS"],
                ["FOREST","FORESTS","FRST"],
                ["FORGE","FORG","FRG"],
                ["FORGES","FRGS"],
                ["FORK","FRK"],
                ["FORKS","FRKS"],
                ["FORT","FT","FRT"],
                ["FREEWAY","FWY","FREEWY","FRWAY","FRWY"],
                ["GARDEN","GDN","GARDN","GRDEN","GRDN"],
                ["GARDENS","GDNS","GRDNS"],
                ["GATEWAY","GTWY","GATEWY","GATWAY","GTWAY"],
                ["GLEN","GLN"],
                ["GLENS","GLNS"],
                ["GREEN","GRN"],
                ["GREENS","GRNS"],
                ["GROVE","GROV","GRV"],
                ["GROVES","GRVS"],
                ["HARBOR","HARB","HBR","HARBR","HRBOR"],
                ["HARBORS","HBRS"],
                ["HAVEN","HVN"],
                ["HEIGHTS","HT","HTS"],
                ["HIGHWAY","HIGHWY","HIWAY","HIWY","HWAY","HWY"],
                ["HILL","HL"],
                ["HILLS","HLS"],
                ["HOLLOW","HLLW","HOLW","HOLLOWS","HOLWS"],
                ["INLET","INLT"],
                ["ISLAND","IS","ISLND"],
                ["ISLANDS","ISS","ISLNDS"],
                ["ISLE","ISLES"],
                ["JUNCTIN","JCT","JCTION","JCTN","JUNCTN","JUNCTON"],
                ["JUNCTIONS","JCTS"],
                ["KEY","KY"],
                ["KEYS","KYS"],
                ["KNL","KNOL","KNOLL"],
                ["KNOLLS","KNLS"],
                ["LK","LAKE"],
                ["LAKES","LKS"],
                ["LAND"],
                ["LANDING","LNDG","LNDNG"],
                ["LANE","LN"],
                ["LGT""LIGHT"],
                ["LIGHTS""LGTS"],
                ["LF""LOAF"],
                ["LCK""LOCK"],
                ["LCKS","LOCKS"],
                ["LDG","LDGE","LODG","LODGE"],
                ["LOOP""LOOPS"],
                ["MALL"],
                ["MNR","MANOR"],
                ["MANORS","MNRS"],
                ["MEADOW","MDW"],
                ["MDWS","MEADOWS","MEDOWS"],
                ["MEWS"],
                ["MILL","ML"],
                ["MILLS","MLS"],
                ["MISSION","MSN","MSSN"],
                ["MOTORWAY","MTWY"],
                ["MNT","MT","MOUNT"],
                ["MNTAIN","MNTN","MOUNTAIN","MOUNTIN","MTIN","MTN"],
                ["MNTNS","MTNS","MOUNTAINS"],
                ["NCK","NECK"],
                ["ORCH","ORCHARD","ORCHRD"],
                ["OVAL","OVL"],
                ["OVERPASS","OPAS"],
                ["PARK","PRK"],
                ["PARKS","PARK"],
                ["PARKWAY","PARKWY","PKWAY","PKWY","PKY","PARKWAYS","PKWYS"],
                ["PASS"],
                ["PASSAGE","PSGE"],
                ["PATH","PATHS"],
                ["PIKE","PIKES"],
                ["PINE","PNE"],
                ["PINES","PNES"],
                ["PLACE","PL"],
                ["PLAIN","PLN"],
                ["PLAINS","PLNS"],
                ["PLAZA","PLZ","PLZA"],
                ["POINT","PT"],
                ["POINTS","PTS"],
                ["PORT","PRT"],
                ["PORTS","PRTS"],
                ["PR","PRAIRIE","PRR"],
                ["RAD","RADIAL","RADIEL","RADL"],
                ["RAMP"],
                ["RANCH","RNCH","RNCH","RNCHS"],
                ["RAPID","RPD"],
                ["RAPIDS","RPDS"],
                ["REST""RST"],
                ["RDG","RDGE","RIDGE"],
                ["RDGS","RIDGES"],
                ["RIV","RIVER","RVR","RIVR"],
                ["RD","ROAD"],
                ["ROADS","RDS"],
                ["ROUTE","RTE"],
                ["ROW"],
                ["RUE"],
                ["RUN"],
                ["SHL","SHOAL"],
                ["SHLS","SHOALS"],
                ["SHOAR","SHORE","SHR"],
                ["SHOARS","SHORES","SHRS"],
                ["SKYWAY","SKWY"],
                ["SPG","SPNG","SPRING","SPRNG"],
                ["SPRINGS","SPGS","SPNGS","SPRNGS"],
                ["SQUARE","SS","SQR","SQRE","SQU"],
                ["SQRS","SQS","SQUARES"],
                ["STATION","STA","STATN","STN"],
                ["STRAVENUE""STRA""STRAV""STRAVEN""STRAVN""STRVN""STRVNUE"],
                ["STREAM","STREME","STRM"],
                ["STREET","STRT","ST","STR"],
                ["STREETS","STS"],
                ["SUMMIT","SMT","SUMIT","SUMITT"],
                ["TERRACE","TER","TERR"],
                ["THROUGHWAY","TRWY"],
                ["TRACE","TRACES","TRCE"],
                ["TRACK","TRAK","TRACKS","TRK","TRKS"],
                ["TRAFFICWAY","TRFY"],
                ["TRAIL","TRAILS","TRL","TRLS"],
                ["TRAILER","TRLR","TRLRS"],
                ["TUNEL","TUNL","TUNLS","TUNNEL","TUNNELS","TUNNL"],
                ["TURNPIKE","TRNPK","TPKE","TURNPK"],
                ["UNDERPASS","UPAS"],
                ["UN","UNION"],
                ["UNIONS","UNS"],
                ["VALLEY","VALLY","VLLY","VLY"],
                ["VALLEYS","VLYS"],
                ["VIADUCT","VDCT","VIA","VIADCT"],
                ["VIEW","VW"],
                ["VIEWS","VWS"],
                ["VILL","VILLAG","VILLAGE","VILLG","VILLIAGE","VLG"],
                ["VILLAGES","VLGS"],
                ["VILLE","VL"],
                ["VIS","VIST","VISTA","VST","VSTA"],
                ["WALKS","WALK"],
                ["WALL"],
                ["WAY","WY"],
                ["WAYS"],
                ["WELL","WL"],
                ["WELLS","WLS"]
               ]
def addycheck(x):

##########################    START: VARIABLE SET UP      ##############################################################################################################################################################################


    if x == "" or len(x) < 2:
        return(ERRORMSG)

    x = (x.upper())                 # sets up uppercase b/c of uppercase address input.
    c = (x.split())                 # splits it up into arrays bc I wanted to do it like that
    c[1] = c[1].lower()
    c[1] = c[1].capitalize()

    randomizercount = 0             #Variable set up randomizercount is how many random letters you want in front
    count = 0                       # counter for how many addresses you used whewn you changed the addresses
    result = ""                     # result for the result
    randaddress1 = ""               # This address will be used when randomizing every 4th digit IE: AAAA 123 ABC ST
    randaddress2 = ""               # This address might be used when randomizing every 4th digit IE: AAAA 123 ABC ST
    fourletters1 = ""                # random 4 letters added infront of addresses
    fourletters2 = ""
#################################   END:   ##############################################################################################################################################################



##########################    START: INCORRECT ADDRESS INPUT HANDLING      ##############################################################################################################################################################################


    if c[-1].isdigit():
        if int(c[-1]) < 1:
            return ("Wrong input, please add a numerical value at the end of each address to specify how many you want.")

        randomizercount = int(c[-1])

        try:
            c = c[0:-1]
        except:
            return(ERRORMSG)

    joined = " ".join(c[0:-1])
    z = 0

#################################   END:   ##############################################################################################################################################################


##########################    START: LOGIC      ##############################################################################################################################################################################

    if c[-1] in "RD":
        ERRMSG = "Next time please use \"Road\" instead of \"RD\" "
        print (joined + " Road" + "\n" +
        joined + " Rd")
        return()

    for Location in range(len(ADDYSHORTCUT)):                     # This checks the big ass array above for matching addresses however, it may have repeats
        if any(c[-1] in d for d in (ADDYSHORTCUT[Location])):     # as a result we have the z to make sure this loop only goes once, when it finds a matching
            for x in ADDYSHORTCUT[Location]:                      # array.
                if len(ADDYSHORTCUT[Location]) >= 2:
                    randaddress1 = joined + " " + (x.lower()).capitalize()
                    randaddress2 = joined + " " + ADDYSHORTCUT[Location][1].lower().capitalize()
                else:
                    randaddress1 = joined + " " + (x.lower()).capitalize()

                count = count + 1
                result = result + (joined + " " + (x.lower()).capitalize() + "\n")
                z = 1

            if z== 1:
                break



    for _ in range(randomizercount - count):
        if _ % 2 == 0:
            for __ in range(4):
                fourletters1 = fourletters1 + (random.choice(string.ascii_uppercase))
            fourletters1 = fourletters1 + " " + randaddress1
            result = result + fourletters1 + "\n"
            fourletters1 = ""

        elif _ % 2 != 0 and randaddress2 != "":
            for __ in range(4):
                fourletters2 = fourletters2 + (random.choice(string.ascii_uppercase))
            fourletters2 = fourletters2 + " " + randaddress2
            result = result + fourletters2 + "\n"
            fourletters2 = ""



#################################   END:   ##############################################################################################################################################################



#################################   RESULT:   ##############################################################################################################################################################

    return (result)

app = Flask(__name__)


def is_request_valid(request):
    is_token_valid = request.form['token'] == 'Z8xEukklpaZWPPWRdd2xyXfg'
    is_team_id_valid = request.form['team_id'] == 'TBLM5TQ4B'


    return is_token_valid and is_team_id_valid


@app.route('/addy', methods=['POST'])
def addy():

    userinput = request.form.get('text')
    response = addycheck(userinput)
    if response == "":
        response = "ERROR COULD NOT BE CHANGED TO ADDRESS"
    if not is_request_valid(request):
        abort(400)

    return jsonify(
        response_type='ephemeral',
        text= response ,)
