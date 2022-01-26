from app import db
from database.models import *
import datetime


class DbWorker:
    def __init__(self):
        pass

    def add_into_db(self, obj):
        db.session.add(obj)
        db.session.commit()

    def add_several_into_db(self, obj_list):
        db.session.add_all(obj_list)
        db.session.commit()


db_work = DbWorker()

toi1 = TypeOfInterests(name="BUSINESS")
toi2 = TypeOfInterests(name="CULTURE")
toi3 = TypeOfInterests(name="ENTERTAINMENT")
toi4 = TypeOfInterests(name="FASHION")
toi5 = TypeOfInterests(name="GASTRONOMY")
toi6 = TypeOfInterests(name="NATURE")
toi7 = TypeOfInterests(name="SPORT")
toi8 = TypeOfInterests(name="EXTREME")
toi9 = TypeOfInterests(name="WATER")

s1 = Sex(gender="Male")
s2 = Sex(gender="Female")

exp1 = ExperienceLevel(experience="Beginner")
exp2 = ExperienceLevel(experience="Medium")
exp3 = ExperienceLevel(experience="Experienced")

transport_type1 = TypeOfTransport(name="TrainStation")
transport_type2 = TypeOfTransport(name="BusStation")
transport_type3 = TypeOfTransport(name="Airplane")

country1 = Country(country="Spain")
country2 = Country(country="France")
country3 = Country(country="Poland")

user1_info = PersonalInfo(city="Warszawa",
                          country_id=country1.id,
                          name="Piotr",
                          sex_id=s1.id,
                          surname="Ziemniaczkiewicz")
user2_info = PersonalInfo(city="Krakow",
                          country_id=country1.id,
                          name="Kasia",
                          sex_id=s2.id,
                          surname="Marchewa")
user3_info = PersonalInfo(city="Toronto",
                          country_id=country2.id,
                          name="Mark",
                          sex_id=s1.id,
                          surname="Baker")
user4_info = PersonalInfo(city="Londyn",
                          country_id=country3.id,
                          name="Romelu",
                          sex_id=s1.id,
                          surname="Lukaku")


user1 = AppUser(login="swiezy_ziemniak",
                email="swiezy_ziemniak@gmail.com",
                personal_info_id=user1_info.id)
user2 = AppUser(login="hejter_najmana",
                email="hejter_najmana@gmail.com",
                personal_info_id=user2_info.id)
user3 = AppUser(login="zwykly_uzytkownik",
                email="zwykly_uzytkownik@gmail.com",
                personal_info_id=user3_info.id)
user4 = AppUser(login="admin",
                email="admin@gmail.com",
                personal_info_id=user4_info.id)
user1.set_password(password="ziemniak1")
user2.set_password(password="boras123")
user3.set_password(password="haslo123")
user4.set_password(password="admin1")

#TODO repair it
'''user1_int0 = user_interests()
user1_int1 = user_interests(user_id=1, interest_id=1)
user1_int2 = user_interests(user_id=1, interest_id=2)
user1_int3 = user_interests(user_id=1, interest_id=3)
user2_int1 = user_interests(user_id=2, interest_id=1)
user2_int2 = user_interests(user_id=2, interest_id=5)
user2_int3 = user_interests(user_id=2, interest_id=7)
user3_int1 = user_interests(user_id=3, interest_id=2)
user3_int2 = user_interests(user_id=3, interest_id=6)
user3_int3 = user_interests(user_id=3, interest_id=8)
user3_int4 = user_interests(user_id=3, interest_id=9)
user4_int1 = user_interests(user_id=4, interest_id=6)
user4_int2 = user_interests(user_id=4, interest_id=9)'''

moderator1 = Moderator("swiezy_ziemniak", "swiezy_ziemniak@gmail.com")
administrator1 = UserAdmin("admin", "admin@gmail.com")
place_admin1 = PlaceAdmin("hejter_najmana", "hejter_najmana@gmail.com")


place1 = Place(place_admin1)
place2 = Place(place_admin1)
place3 = Place(place_admin1)

geo1 = GeoInformation(country="Barcelona", language="Spanish, Catalan", region="Catalonia")
geo2 = GeoInformation(country="Paris", language="French", region="Ile-de-France")
geo3 = GeoInformation(country="Warsaw", language="Polish", region="Mazowieckie")

attraction1 = Attraction()
attraction2 = Attraction()
attraction3 = Attraction()

photo1 = Photo(post_id=1, attraction_id=1, photo_path=r"C:\Users\Maciek\Pictures\photo1")
photo2 = Photo(post_id=2, attraction_id=2, photo_path=r"C:\Users\Maciek\Pictures\photo2")
photo3 = Photo(post_id=3, attraction_id=3, photo_path=r"C:\Users\Maciek\Pictures\photo3")

weather1 = Weather(place_id=1, cloudiness=1, temperature=39, humidity=6, date="05 Jul 2021")
weather2 = Weather(place_id=2, cloudiness=7, temperature=10, humidity=7, date="07 Dec 2021")
weather3 = Weather(place_id=3, cloudiness=11, temperature=-2, humidity=8, date="21 Jan 2022")

address1 = Address(country_id=1,
                   city="Barcelona",
                   google_maps_link="https://www.google.com/maps/place/Barcelona,+Prowincja+Barcelona,+Hiszpania/@41.3927755,2.0701494,12z/data=!3m1!4b1!4m5!3m4!1s0x12a49816718e30e5:0x44b0fb3d4f47660a!8m2!3d41.3873974!4d2.168568",
                   street="Carrer de Casp",
                   nr_of_street=12,
                   nr_of_apartment=7,
                   postcode="08-010")
address2 = Address(country_id=2,
                   city="Paris",
                   google_maps_link="https://www.google.com/maps/place/Point+Driving+Jussieu/@48.8452445,2.3545754,20.08z/data=!4m13!1m7!3m6!1s0x47e66e1f06e2b70f:0x40b82c3688c9460!2zUGFyecW8LCBGcmFuY2ph!3b1!8m2!3d48.856614!4d2.3522219!3m4!1s0x47e671effcb288f9:0x3ff6b8e0ad30e8f5!8m2!3d48.8453193!4d2.3544759",
                   street="Rue Linne",
                   nr_of_street=27,
                   nr_of_apartment=27,
                   postcode="75-005")
address3 = Address(country_id=3,
                   city="Warsaw",
                   google_maps_link="https://www.google.com/maps/place/Pu%C5%82awska+15,+00-791+Warszawa/@52.2104462,21.0203171,17z/data=!3m1!4b1!4m5!3m4!1s0x471eccde57ea4eb5:0x1feb91ecede26b49!8m2!3d52.2104429!4d21.0225058",
                   street="Pulawska",
                   nr_of_street=15,
                   nr_of_apartment=2,
                   postcode="00-791")

hotel1 = Hotel(place_id=1,
               address_id=1,
               name="Novotel Barcelona City",
               note=1,
               site_link="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.google.com%2Faclk%3Fsa%3Dl%26ai%3DCTRIfNnDwYdrLI8-viQadjYboDZ7Lsb9c_bqOg_EJ44mYndUQCAoQAigEYOkEoAGGqYn-AqkCFW9kHvnzsj6oAwWqBEdP0OoVgxzXRYuRa03_J8P0NjAcK2vJGcwqpWApKvwwc7neYr22Th7oBBJ92Q8m5JWz1e96IP28NYPFRU5ywXIuePZYRxqq58AEpK6fxbICiAXR0vHjB8AFkgGgBmWIBwGQBwLICawBogqEAQoKMjAyMi0wMS0yNxABGgJQTClX65JTZZRuujIFYWNjb3I4AkgBUghRRUIxUkEyMl0AAKBCZWZmVkFyA0VVUoIBCQoDUUVCMgIIArABAbgBBMgBr4LaL9oBDG1lbWJlcnNfb25seeABAugBAvABAfgBAaACAOACAOoCA1BMTvACAYoDAOgKA5ALA9ALGrgMAdAVAYAXAQ%26sig%3DAOD64_0HiSaWMogaBJynV_mJFnNMsb1jvg%26adurl%3Dhttps%3A%2F%2Ftravel-productads.koddi.com%2FPropertyAdvocateAPI%2FClickRedirect%253Fclient%253DAccor%2526channel%253DGHPA%2526placement%253Dlocaluniversal%2526campaign%253D2088528209%2526destinationURL%253Dhttps%25253A%25252F%25252Fall.accor.com%25252Flien_externe.svlt%25253Fgoto%25253Drech_resa%252526destination%25253D5560%252526dayIn%25253D27%252526monthIn%25253D01%252526yearIn%25253D2022%252526nightNb%25253D1%252526adultNumber%25253D2%252526childrenNumber%25253D0%252526merchantid%25253DRT-FR018138-%252526sourceid%25253Dx-5560-PL-cpa-desktop-default-0--1-27-01-2022-2-Thursday-localuniversal-2088528209-0-0-1%252526utm_source%25253DGoogle%25252BHotel%25252BAds%252526utm_medium%25253Dpartenariats%252526utm_campaign%25253D5560-PL-cpa-desktop-default-0--localuniversal-2088528209-0-0-1%26ctype%3D268&psig=AOvVaw1U-qRpLBncRaKjqrVgdqos&ust=1643233718354000&cd=&rct=j&ved=2ahUKEwiCwuXh8M31AhXiSpEFHTM5DWQQx94CegQIARBk")
hotel2 = Hotel(place_id=2,
               address_id=2,
               name="Hotel Montparnasse Alesia",
               note=2,
               site_link="https://www.booking.com/searchresults.pl.html?aid=1288294;label=metagha-link-LUPL-hotel-50444_dev-desktop_los-1_bw-2_dow-Thursday_defdate-1_room-0_gstadt-2_rateid-0_aud-0_gacid-6642513966_mcid-50_ppa-0_clrid-0_ad-1_gstkid-0_checkin-20220127_lp-1011419_r-18388696721445413327;sid=2d2763c783efcad0952803cc0f808f18;checkin=2022-01-27;checkout=2022-01-28;city=-1456928;ext_price_total=322.26;group_children=0;highlighted_hotels=50444;hlrd=with_dates;keep_landing=1;redirected=1;show_room=5044402_203485355_0_2_0;source=hotel&gclid=CjwKCAiA3L6PBhBvEiwAINlJ9ETwa55_hme1JtEEMRcohmaCiSGvGNg6oqqLeP77mgOVUSAC65QdrhoC26kQAvD_BwE&utm_campaign=PL&utm_content=dev-desktop_los-1_bw-2_dow-Thursday_defdate-1_room-0_gstadt-2_rateid-0_aud-0_gacid-6642513966_mcid-50_ppa-0_clrid-0_ad-1_gstkid-0_checkin-20220127&utm_medium=localuniversal&utm_source=metagha&utm_term=hotel-50444&room1=A,A,;")
hotel3 = Hotel(place_id=3,
               address_id=3,
               name="NYX Hotel Warsaw",
               note=3,
               site_link="https://www.leonardo-hotels.com/booking?hotel=nyx-hotel-warsaw&from=2022-01-30T00:00:00&to=2022-01-31T00:00:00&stay=leisure&redeemPoints=false&paxesConfig=adults,2,children,0,infants,0&RefFrom=GoogleHPA&utm_source=google&site=localuniversal&dsclid=42724493144653824")

transport1 = Transport(type_id=1,
                       place_id=1,
                       address_id=1,
                       name="Barcelona Metro",
                       site_link="https://mybarcelona.pl/metro/")
transport2 = Transport(type_id=4,
                       place_id=2,
                       address_id=2,
                       name="Paris Charles de Gaulle Airport",
                       site_link="https://www.parisaeroport.fr/en")
transport3 = Transport(type_id=2,
                       place_id=3,
                       address_id=3,
                       name="Train Warsaw",
                       site_link="https://www.ztm.waw.pl/")


visit1 = Visit()
visit2 = Visit()
visit3 = Visit()

post1 = Post(creator_id=1, creation_date=datetime.date(2021, 6, 6), text="best trip ever")
post2 = Post(creator_id=2, creation_date=datetime.date(2022, 1, 1), text="Fajniutko")
post3 = Post(3)

comment1 = Comment(text="Dzien dobry nie lubie byc niemily")
comment2 = Comment(text="Fantastyczne widoki")
comment3 = Comment(text="dogonilismy kroliczka!! :DD")


settlement1 = Settlement(stage="undetermined")
settlement2 = Settlement(stage="rejected")
settlement3 = Settlement(stage="accepted")

post_report1 = PostReport(moderator_id=1,
                          settlement=1,
                          reporter_id=1,
                          post_id=1,
                          reason="Niedobry byl")
post_report2 = PostReport(moderator_id=2,
                          settlement=2,
                          reporter_id=2,
                          post_id=2,
                          reason="Bardzo brzydki")
post_report3 = PostReport(moderator_id=3,
                          settlement=3,
                          reporter_id=3,
                          post_id=3,
                          reason="Obrzydliwy")

comment_report1 = CommentReport(moderator_id=1,
                                settlement=1,
                                reporter_id=3,
                                comment_id=1,
                                reason="sad comment :(")
comment_report2 = CommentReport(moderator_id=1,
                                settlement=2,
                                reporter_id=3,
                                comment_id=2,
                                reason="sad")
comment_report3 = CommentReport(moderator_id=1,
                                settlement=3,
                                reporter_id=3,
                                comment_id=3,
                                reason="he was angry!!")

user_report1 = UserReport(user_admin_id=1,
                          settlement=1,
                          reporter_id=1,
                          reported_id=3,
                          reason="Madness")
user_report2 = UserReport(user_admin_id=1,
                          settlement=1,
                          reporter_id=1,
                          reported_id=3,
                          reason="he is not normal")
user_report3 = UserReport(user_admin_id=1,
                          settlement=3,
                          reporter_id=1,
                          reported_id=3,
                          reason="idk what's wrong with him")

place_report1 = PlaceReport(place_admin_id=1,
                            settlement=1,
                            reporter_id=3,
                            place_id=1,
                            reason="i dont like it, my gf broke up with me here")
place_report2 = PlaceReport(place_admin_id=2,
                            settlement=2,
                            reporter_id=3,
                            place_id=2,
                            reason="This place does not exist")
place_report3 = PlaceReport(place_admin_id=3,
                            settlement=3,
                            reporter_id=3,
                            place_id=3,
                            reason="idk what's that")
