import requests
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup as bs


#Login information
username = input("Please enter your NRIC.")
pin = input("Please enter your password.")
#date = "Please enter the date you wish to check slots on."

#Request Token
s = requests.Session()
r = s.get ("https://www.ssdcl.com.sg")
r = s.get("https://www.ssdcl.com.sg/User/Login")
soup = bs(r.text, 'html.parser')
loginToken = soup.findAll(attrs={"name" : "__RequestVerificationToken"})[0]['value']

#Data
lesson_date = []
lesson_time = []
lesson_id = []


#Create login information payload
login_payload = {
    "__RequestVerificationToken" : loginToken,
    "UserName" : username,
    "Password" : pin,
    "returnUrl" : "https://ssdcl.com.sg/user-action/?action=login&returnUrl=https://www.ssdcl.com.sg/User/Information",
}

#Post Payload
r = s.post("https://www.ssdcl.com.sg/Account/Login", data = login_payload)

#Request page before booking page
r = s.get("https://www.ssdcl.com.sg/User/Booking/BookingList")


#Request Booking Page and Token
r = s.get("https://www.ssdcl.com.sg/User/Booking/AddBooking?bookingType=PL")
soup = bs(r.text, "html.parser")
checkingToken = soup.findAll(attrs={"name" : "__RequestVerificationToken"})[0]["value"]
form = soup.find("form", {"id": "formCourseSelect"})

#Create checking information payload
checking_payload = {
    "__RequestVerificationToken" : checkingToken,
    "SlotId" : "0",
    "SelectedSessionNumber" : "0",
    "SellBundleId" : "00000000-0000-0000-0000-000000000000",
    "IsOrientation" : "False",
    "BookingType" : "PL",
    "SelectedDate" : "10 Jul 2020", #Change to allow users to set date as desired
    "SelectedSessionType" : "R",
    "SelectedLocation" : "Woodlands",
    "CarModelId" : "1",
    "IsFiRequired" : "False",
    "FixedInstructor" : "" ,
    "checkEligibility" : "CHECK_SLOT_AVAILABLE",

}

#Post booking payload to booking page
r = s.post("https://www.ssdcl.com.sg/User/Booking/AddBooking", data = checking_payload)

#Find slots available 
soup = bs(r.text, "html.parser")
a = soup.findAll("tr")
for item in a:
    dates = item.find("a")
    if dates != None:
        lesson_date.append(f"Date = {dates.text}")
    booking = item.findAll("td")
    for time in booking:
        lesson_time.append(time.text.replace("✔", " ").strip())

for slots in soup.findAll(attrs={"class" : "pb-15 text-center"}):
    tags = slots.find("a", attrs={"id",True})
    if tags:
        lesson_id.append(tags.attrs["id"].split("_")[0])

#print (lesson_date)
#print (lesson_id)
#print (lesson_time)



r = s.get("https://www.ssdcl.com.sg/User/Booking/AddBooking")
soup = bs(r.text, "html.parser")
bookingToken = soup.findAll(attrs={"name" : "__RequestVerificationToken"})[0]["value"]
form = soup.find("form", {"id": "formCourseSelect"})

booking_payload = {
    "__RequestVerificationToken" : checkingToken,
    "SlotId" : "0", #currently slotID is hardcoded
    "SelectedSessionNumber" : "1",
    "SellBundleId" : "00000000-0000-0000-0000-000000000000",
    "IsOrientation" : "False",
    "BookingType" : "PL",
    "SelectedDate" : "10/7/2020 12:00:00 AM", #Change to allow users to set date as desired
    "SelectedSessionType" : "R",
    "SelectedLocation" : "Woodlands",
    "CarModelId" : "1",
    "IsFiRequired" : "False",
    "FixedInstructor" : "" ,
    "SelectedNoOfDaysToDisplays" : "7",

}

r = s.post("https://www.ssdcl.com.sg/User/Booking/AddBooking", data = booking_payload)

r = s.get("https://www.ssdcl.com.sg/User/Payment/ReviewItems")

r = s.get("https://www.ssdcl.com.sg/User/Payment/ConfirmPurchase")

soup = bs(r.text, "html.parser")
cartID = soup.find(attrs={"name" : "ShoppingCartItemIds"})["value"]

r = s.get("https://www.ssdcl.com.sg/User/Payment/MakePayment")
soup = bs(r.text, "html.parser")
checkoutToken = soup.findAll(attrs={"name" : "__RequestVerificationToken"})[0]["value"]
form = soup.find("form", {"id": "frmMakePayment"})

checkout_payload = {
    "__RequestVerificationToken" : checkoutToken,
    "ShoppingCartItemIds" : cartID
}

r = s.post("https://www.ssdcl.com.sg/User/Payment/MakePayment", data = checkout_payload)




