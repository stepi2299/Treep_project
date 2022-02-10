from app import db
from database.models import *
import datetime


class DbWorker:
    def __init__(self):
        pass

    def fill_db_with_default_values(self):
        pass

    @staticmethod
    def delete_singe_record(obj):
        try:
            db.session.delete(obj)
            db.session.commit()
        except:
            db.session.rollback()

    @staticmethod
    def delete_all_records_from_table(model):
        try:
            model.query.delete()
            db.session.commit()
        except:
            db.session.rollback()

    @staticmethod
    def add_into_db(obj):
        try:
            if isinstance(obj, list):
                db.session.add_all(obj)
            else:
                db.session.add(obj)
            db.session.commit()
        except:
            db.session.rollback()


def fill_with_mandatory_data():
    toi1 = TypeOfInterests(name="BUSINESS")
    toi2 = TypeOfInterests(name="CULTURE")
    toi3 = TypeOfInterests(name="ENTERTAINMENT")
    toi4 = TypeOfInterests(name="FASHION")
    toi5 = TypeOfInterests(name="GASTRONOMY")
    toi6 = TypeOfInterests(name="NATURE")
    toi7 = TypeOfInterests(name="SPORT")
    toi8 = TypeOfInterests(name="EXTREME")
    toi9 = TypeOfInterests(name="WATER")
    db.session.add_all([toi1, toi2, toi3, toi4, toi5, toi6, toi7, toi8])
    db.session.commit()

    s1 = Sex(gender="Male")
    s2 = Sex(gender="Female")
    db.session.add_all([s1, s2])
    db.session.commit()

    exp1 = ExperienceLevel(experience="Beginner")
    exp2 = ExperienceLevel(experience="Medium")
    exp3 = ExperienceLevel(experience="Experienced")
    db.session.add_all([exp1, exp2, exp3])
    db.session.commit()

    transport_type1 = TypeOfTransport(name="TrainStation")
    transport_type2 = TypeOfTransport(name="BusStation")
    transport_type3 = TypeOfTransport(name="Airplane")
    db.session.add_all([exp1, exp2, exp3])
    db.session.commit()

    country1 = Country(country="Poland")
    country2 = Country(country="Canada")
    country3 = Country(country="England")
    country4 = Country(country="USA")
    db.session.add_all([country1, country2, country3])
    db.session.commit()

    profile_photo1 = ProfilePhoto(photo_path="app/static/img/profilowe.jpg")
    db.session.add(profile_photo1)
    db.session.commit()

    user1_info = PersonalInfo(
        city="Warszawa",
        country_id=country1.id,
        name="Piotr",
        sex_id=s1.id,
        surname="Ziemniaczkiewicz",
    )
    user2_info = PersonalInfo(
        city="Krakow",
        country_id=country1.id,
        name="Kasia",
        sex_id=s2.id,
        surname="Marchewa",
    )
    user3_info = PersonalInfo(
        city="Toronto",
        country_id=country2.id,
        name="Mark",
        sex_id=s1.id,
        surname="Baker",
    )
    user4_info = PersonalInfo(
        city="Londyn",
        country_id=country3.id,
        name="Romelu",
        sex_id=s1.id,
        surname="Lukaku",
    )
    db.session.add_all([user1_info, user2_info, user3_info, user4_info])
    db.session.commit()

    user1 = AppUser(
        login="swiezy_ziemniak",
        email="swiezy_ziemniak@gmail.com",
        experience=12,
        personal_info_id=user1_info.id,
    )
    user2 = AppUser(
        login="hejter_najmana",
        email="hejter_najmana@gmail.com",
        experience=123,
        personal_info_id=user2_info.id,
    )
    user3 = AppUser(
        login="zwykly_uzytkownik",
        email="zwykly_uzytkownik@gmail.com",
        experience=1234,
        personal_info_id=user3_info.id,
    )
    user4 = AppUser(
        login="admin",
        email="admin@gmail.com",
        experience=1234,
        personal_info_id=user4_info.id,
    )
    user1.set_password(password="ziemniak1")
    user2.set_password(password="boras123")
    user3.set_password(password="haslo123")
    user4.set_password(password="admin1")
    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()

    z_inf1 = PersonalInfo(
        city="Sieradz",
        country_id=country1.id,
        name="Karol",
        sex_id=s1.id,
        surname="Krawczyk",
    )
    z_inf2 = PersonalInfo(
        city="Warszawa",
        country_id=country2.id,
        name="Twoja",
        sex_id=s2.id,
        surname="Stara",
    )
    z_inf3 = PersonalInfo(
        city="Kanal",
        country_id=country1.id,
        name="Tadeusz",
        sex_id=s1.id,
        surname="Norek",
    )
    db.session.add_all([z_inf1, z_inf2, z_inf3])
    db.session.commit()

    moderator1 = Moderator(
        login="moderatorek", email="motorek@gamil.com", personal_info_id=z_inf1.id
    )
    moderator1.set_password("moderatorek")
    db.session.add(moderator1)
    db.session.commit()
    administrator1 = UserAdmin(
        login="adi", email="add@gamil.com", personal_info_id=z_inf2.id
    )
    administrator1.set_password("adminek")
    db.session.add(administrator1)
    db.session.commit()
    place_admin1 = PlaceAdmin(
        login="adminek", email="adminek@gamil.com", personal_info_id=z_inf3.id
    )
    place_admin1.set_password("adminek_miejsc")
    db.session.add(place_admin1)
    db.session.commit()

    place1 = Place(name="Barcelona", admin_id=place_admin1.id, country_id=country1.id, language="Spanish, Catalan", region="Catalonia")
    place2 = Place(name="Paris", admin_id=place_admin1.id, country_id=country2.id, language="French", region="Ile-de-France")
    place3 = Place(name="Warszawa", admin_id=place_admin1.id, country_id=country3.id, language="Polish", region="Mazowieckie")

    db.session.add_all([place1, place2, place3])
    db.session.commit()

    place1.add_attraction(
        name="Camp Nou",
        description="Pieknie graja",
        photo_path="app/static/img/campnou.jpg",
        admin_id=place_admin1.id,
        site_link="https://www.fcbarcelona.com/en/club/facilities/camp-nou",
        google_maps='https://www.google.com/maps/place/Barcelona,+Prowincja+Barcelona,+Hiszpania/@41.3927755,2.0701494,12z/data=!3m1!4b1!4m5!3m4!1s0x12a49816718e30e5:0x44b0fb3d4f47660a!8m2!3d41.3873974!4d2.168568"',
    )

    place2.add_attraction(
        name="Eiffel Tower",
        description="Piekna wieza",
        photo_path="app/static/img/eifel.jpg",
        admin_id=place_admin1.id,
        site_link="https://www.toureiffel.paris/fr",
        google_maps="https://www.google.com/maps/place/Wie%C5%BCa+Eiffla/@48.8583701,2.2944813,15z/data=!4m5!3m4!1s0x0:0x8ddca9ee380ef7e0!8m2!3d48.8583701!4d2.2944813",
    )

    place3.add_attraction(
        name="Palac kultury i nauki",
        description="piekny palac",
        photo_path="app/static/img/pkin.jpg",
        admin_id=place_admin1.id,
        site_link="https://pkin.pl/",
        google_maps="https://www.google.com/maps/place/Pa%C5%82ac+Kultury+i+Nauki/@52.231838,21.005995,15z/data=!4m5!3m4!1s0x0:0xc2e97ae5311f2dc2!8m2!3d52.231838!4d21.005995",
    )

    db.session.add_all([place1, place2, place3])
    db.session.commit()

    weather1 = Weather(
        place_id=place1.id,
        cloudiness=1,
        temperature=39,
        humidity=6,
        date=datetime.date(2021, 6, 22),
    )
    weather2 = Weather(
        place_id=place2.id,
        cloudiness=7,
        temperature=10,
        humidity=7,
        date=datetime.date(21, 6, 12),
    )
    weather3 = Weather(
        place_id=place3.id,
        cloudiness=11,
        temperature=-2,
        humidity=8,
        date=datetime.date(21, 2, 2),
    )
    db.session.add_all([weather1, weather2, weather3])
    db.session.commit()

    address1 = Address(
        country_id=country1.id,
        city="Barcelona",
        google_maps_link="https://www.google.com/maps/place/Barcelona,+Prowincja+Barcelona,+Hiszpania/@41.3927755,2.0701494,12z/data=!3m1!4b1!4m5!3m4!1s0x12a49816718e30e5:0x44b0fb3d4f47660a!8m2!3d41.3873974!4d2.168568",
        street="Carrer de Casp",
        nr_of_street="12a",
        nr_of_apartment=7,
        postcode="08-010",
    )
    address2 = Address(
        country_id=country2.id,
        city="Paris",
        google_maps_link="https://www.google.com/maps/place/Point+Driving+Jussieu/@48.8452445,2.3545754,20.08z/data=!4m13!1m7!3m6!1s0x47e66e1f06e2b70f:0x40b82c3688c9460!2zUGFyecW8LCBGcmFuY2ph!3b1!8m2!3d48.856614!4d2.3522219!3m4!1s0x47e671effcb288f9:0x3ff6b8e0ad30e8f5!8m2!3d48.8453193!4d2.3544759",
        street="Rue Linne",
        nr_of_street="27",
        nr_of_apartment=27,
        postcode="75-005",
    )
    address3 = Address(
        country_id=country3.id,
        city="Warsaw",
        google_maps_link="https://www.google.com/maps/place/Pu%C5%82awska+15,+00-791+Warszawa/@52.2104462,21.0203171,17z/data=!3m1!4b1!4m5!3m4!1s0x471eccde57ea4eb5:0x1feb91ecede26b49!8m2!3d52.2104429!4d21.0225058",
        street="Pulawska",
        nr_of_street="15/2",
        nr_of_apartment=2,
        postcode="00-791",
    )
    db.session.add_all([address1, address2, address3])
    db.session.commit()

    hotel1 = Hotel(
        place_id=place1.id,
        address_id=address1.id,
        name="Novotel Barcelona City",
        note=1,
        site_link="https://www.guestreservations.com/novotel-barcelona-city/",
        admin_id=place_admin1.id,
    )
    place1.hotels.append(hotel1)
    hotel2 = Hotel(
        place_id=place2.id,
        address_id=address2.id,
        name="Hotel Montparnasse Alesia",
        note=2,
        site_link="https://www.hotelsaphirgrenelle.fr/en/",
        admin_id=place_admin1.id,
    )
    place2.hotels.append(hotel2)
    hotel3 = Hotel(
        place_id=place3.id,
        address_id=address3.id,
        name="NYX Hotel Warsaw",
        note=3,
        site_link="https://www.leonardo-hotels.com/",
        admin_id=place_admin1.id,
    )
    place3.hotels.append(hotel3)
    db.session.add_all([hotel1, hotel2, hotel3])
    db.session.commit()

    transport1 = Transport(
        type_id=transport_type2.id,
        place_id=place1.id,
        address_id=address1.id,
        name="Barcelona Bus Station",
        site_link="https://barcelonanord.barcelona/en",
        admin_id=place_admin1.id,
    )
    transport2 = Transport(
        type_id=transport_type3.id,
        place_id=place2.id,
        address_id=address2.id,
        name="Paris Charles de Gaulle Airport",
        site_link="https://www.parisaeroport.fr/en",
        admin_id=place_admin1.id,
    )
    transport3 = Transport(
        type_id=transport_type1.id,
        place_id=place3.id,
        address_id=address3.id,
        name="Train Warsaw",
        site_link="https://www.ztm.waw.pl/",
        admin_id=place_admin1.id,
    )
    db.session.add_all([transport1, transport2, transport3])
    db.session.commit()

    visit1 = Visit(
        place_id=place1.id,
        hotel_id=hotel1.id,
        transport_id=transport1.id,
        user_id=user1.id,
        name="Wycieczka do hyszpanii z krystyna w 2012",
        start_date=datetime.date(2014, 6, 5),
        end_date=datetime.date(2014, 6, 12),
    )
    visit11 = Visit(
        place_id=place1.id,
        hotel_id=hotel1.id,
        transport_id=transport1.id,
        user_id=user1.id,
        name="Wycieczka do hyszpanii z twoim tym w 2013",
        start_date=datetime.date(2013, 6, 5),
        end_date=datetime.date(2013, 6, 12),
    )
    attraction1 = Attraction.query.get(1)
    visit1.attractions.append(attraction1)
    visit2 = Visit(
        place_id=place2.id,
        hotel_id=hotel2.id,
        transport_id=transport2.id,
        user_id=user2.id,
        name="do paryza samemu bo jestem sam chlip chlip",
        start_date=datetime.date(2021, 1, 18),
        end_date=datetime.date(2021, 1, 28),
    )
    attraction2 = Attraction.query.get(2)
    visit2.attractions.append(attraction2)
    visit3 = Visit(
        place_id=place3.id,
        hotel_id=hotel3.id,
        transport_id=transport3.id,
        user_id=user3.id,
        name="wyjscie z domu po prostu",
        start_date=datetime.date(2022, 1, 28),
        end_date=datetime.date(2022, 1, 28),
    )
    attraction3 = Attraction.query.get(3)
    visit3.attractions.append(attraction3)
    db.session.add_all([visit1, visit2, visit3, visit11])
    db.session.commit()

    post1 = Post(
        creator_id=user1.id, text="best trip ever", visit_id=visit1.id, note=90
    )
    post2 = Post(
        creator_id=user2.id, text="fajnie fajniutko", visit_id=visit2.id, note=60
    )
    post3 = Post(
        creator_id=user3.id,
        text="spoko bo tylko z domu na chwile wyszedlem",
        visit_id=visit3.id,
        note=20,
    )
    db.session.add_all([post1, post2, post3])
    db.session.commit()

    photo1 = Photo(post_id=1, photo_path=r"app/static/img/campnou.jpg")
    photo2 = Photo(post_id=2, photo_path=r"app/static/img/eifel.jpg")
    photo3 = Photo(post_id=3, photo_path=r"app/static/img/pkin.jpg")
    db.session.add_all([photo1, photo2, photo3])
    db.session.commit()

    comment1 = Comment(
        creator_id=user3.id,
        post_id=post1.id,
        text="Dzien dobry nie lubie byc niemily",
        note=1,
    )
    comment2 = Comment(
        creator_id=user3.id, post_id=post2.id, text="Fantastyczne widoki", note=-1,
    )
    comment3 = Comment(
        creator_id=user3.id,
        post_id=post3.id,
        text="dogonilismy kroliczka!! :DD",
        note=2,
    )
    db.session.add_all([comment1, comment2, comment3])
    db.session.commit()

    settlement1 = Settlement(stage="undetermined")
    settlement2 = Settlement(stage="rejected")
    settlement3 = Settlement(stage="accepted")
    db.session.add_all([settlement1, settlement2, settlement3])
    db.session.commit()

    post_report1 = PostReport(
        reporter_id=user3.id,
        reason="Niedobry byl",
        interaction_id=post1.id,
        settlement_id=settlement1.id,
        moderator_id=moderator1.id,
    )
    post_report2 = PostReport(
        reporter_id=user3.id,
        reason="Bardzo brzydki",
        interaction_id=post2.id,
        settlement_id=settlement2.id,
        moderator_id=moderator1.id,
    )
    post_report3 = PostReport(
        reporter_id=user3.id,
        reason="Obrzydliwy",
        interaction_id=post3.id,
        settlement_id=settlement3.id,
        moderator_id=moderator1.id,
    )
    db.session.add_all([post_report1, post_report2, post_report3])
    db.session.commit()

    comment_report1 = CommentReport(
        reporter_id=user3.id, reason="sad comment :(", interaction_id=comment1.id,
    )
    comment_report2 = CommentReport(
        reporter_id=user3.id, reason="sjdfgbsdngikfgdj", interaction_id=comment2.id
    )
    comment_report3 = CommentReport(
        reporter_id=user3.id,
        reason="obrazil mn i moja kolezanke dziad",
        interaction_id=comment3.id,
        settlement_id=settlement3.id,
        moderator_id=moderator1.id,
    )
    db.session.add_all([comment_report1, comment_report2, comment_report3])
    db.session.commit()

    user_report1 = UserReport(
        reporter_id=user3.id,
        reason="Madness",
        reported_id=user1.id,
        settlement_id=settlement1.id,
        user_admin_id=administrator1.id,
    )
    user_report2 = UserReport(
        reporter_id=user3.id, reason="he's not normal", reported_id=user2.id
    )
    user_report3 = UserReport(
        reporter_id=user3.id, reason="AAAAAAAAAAAAAAAAAAAAA", reported_id=user3.id
    )
    db.session.add_all([user_report1, user_report2, user_report3])
    db.session.commit()

    place_report1 = PlaceReport(
        reporter_id=user3.id,
        reason="i dont like it, my gf broke up with me here",
        place_id=place1.id,
    )
    place_report2 = PlaceReport(
        reporter_id=user3.id, reason="this place dont exist", place_id=place2.id
    )
    place_report3 = PlaceReport(
        reporter_id=user3.id,
        reason="looks like i was in russia",
        place_id=place3.id,
        settlement_id=settlement3.id,
        admin_id=place_admin1.id,
    )
    db.session.add_all([place_report1, place_report2, place_report3])
    db.session.commit()

    user1.interest.append(toi1)
    user1.interest.append(toi2)
    user1.interest.append(toi3)
    user2.interest.append(toi4)
    user2.interest.append(toi5)
    user2.interest.append(toi3)
    user4.interest.append(toi9)
    user4.interest.append(toi8)
    user1.follow(user2)
    user1.follow(user3)
    user3.follow(user4)
    user4.follow(user3)
    user4.follow(user1)
    attraction1.interested.append(toi1)
    attraction1.interested.append(toi2)
    attraction1.interested.append(toi4)
    attraction2.interested.append(toi6)
    attraction2.interested.append(toi7)
    attraction2.interested.append(toi3)
    attraction3.interested.append(toi8)
    attraction3.interested.append(toi6)
    attraction3.interested.append(toi3)
    visit1.attractions.append(attraction1)
    visit2.attractions.append(attraction2)
    visit3.attractions.append(attraction3)

    db.session.add_all(
        [
            user1,
            user2,
            user3,
            user4,
            attraction1,
            attraction2,
            attraction3,
            visit1,
            visit2,
            visit3,
        ]
    )
    db.session.commit()


fill_with_mandatory_data()
