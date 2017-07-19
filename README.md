# Ipsut

Ipsut is a simple webapp for setting up/tracking user check-ins using QR codes. It is written in Python using the Flask framework.

Written by [Jason Rigden](https://jasonrigden.com/) and [Daniel Kraft](http://frigginglorio.us/) for the [2017 AngelHack Global Hackathon Series: Seattle](http://angelhack.com/angelhack-global-hackathon-series-seattle)

It is live and available at [http://ipsut.frigginglorio.us](http://ipsut.frigginglorio.us)

## Usage
Ipsut allows you to create "Events" that have a series of check-in "Sheets". A check-in sheet consists of a QR Code, basic info (a title and description), and an optional map via the [HERE API](https://developer.here.com/) with coordinates in lattitude/longitude.

The application currently allows admin users to create the events and sheets, shows them a printout of the QR code associated with it. The admin is then able to go to their specified location and display the code. Any logged-in user who scans the QR code with their phone is then given a "Point" in the event, and is added to the Event and global leaderboards.

Common use cases include tracking users for prize drawings in a pubcrawl or treasure hunt.

## Development

```
git clone https://github.com/ipsut/ipsut
cd ipsut
pip install -r requirements.txt
python webapp.py
```


## TODO

1. Setup OAuth (currently login system is a sham. to log in as admin to view created QR codes for printing, simply navigate to /signin with username admin, and any password)
2. Flesh out event management. Create "events" table/model with user access controls.
3. Fix UI/make less confusing. Fix mobile page navigation.

## Etymology
Ipsut is a Pacific Northwest Native American word meaning "hidden place". It is pronounced ["Ipsoot"](https://books.google.com/books?id=xv4qlIPaSLUC&pg=PA113&lpg=PA113&dq=Ipsut+hidden+place&source=bl&ots=mFHViOYdRm&sig=a_Gguo0H_q_74hl6VNmNITN98To&hl=en&sa=X&ved=0ahUKEwjKlPzNmpbVAhUCLmMKHSiKA1YQ6AEIQTAE#v=onepage&q=Ipsut%20hidden%20place&f=false).