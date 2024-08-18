# Restaurants search

## Introduction

This python script is used to search for all the restaurants in a rectangluar shape area and output them in to a .csv file to statistical use. The main data source is Google, so a payment method is required when using this service. Mild use won't cause any fee. For more information, please refer to: [Places API Usage and Billing](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing#basic-nearbysearch)

## Data

Output is in the format of a list of JSON files and a CSV(Comma-separated values) file. Data in JSON(JavaScript Object Notation) files is the raw http response from API requests. Data in the CSV file is generated from the JSON files, with duplicated rows being removed.

Information Types:

> **The following fields trigger the Nearby Search (Basic) SKU:**
> accessibilityOptions, addressComponents, adrFormatAddress, attributions, businessStatus, displayName, formattedAddress, googleMapsUri, iconBackgroundColor, iconMaskBaseUri, id, location, name, photos, plusCode, primaryType, primaryTypeDisplayName, shortFormattedAddress, subDestinations, types, utcOffsetMinutes, viewport
> The name field contains the place resource name in the form: places/PLACE_ID. Use displayName to access the text name of the place.
> **The following fields trigger the Nearby Search (Advanced) SKU:**
> currentOpeningHours, currentSecondaryOpeningHours, internationalPhoneNumber, nationalPhoneNumber, priceLevel, rating, regularOpeningHours, regularSecondaryOpeningHours, userRatingCount, websiteUri
> **The following fields trigger the Nearby Search (Preferred) SKU:**
> allowsDogs, curbsidePickup, delivery, dineIn, editorialSummary, evChargeOptions, fuelOptions, goodForChildren, goodForGroups, goodForWatchingSports, liveMusic, menuForChildren, parkingOptions, paymentOptions, outdoorSeating, reservable, restroom, reviews, servesBeer, servesBreakfast, servesBrunch, servesCocktails, servesCoffee, servesDessert, servesDinner, servesLunch, servesVegetarianFood, servesWine, takeout

## Search Strategy

(Illustration to be added)
