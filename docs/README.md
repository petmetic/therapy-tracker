# Project Brief for Therapy tracker

## What

An app that helps you keep your client's therapy history up to date.

- App Name : Therapy tracker
- Customer : Alenka masaže
- Development Team : Meta Petrič
- Design Team : ______
- Web URL : _______

## Why

The client expressed a need for an online tracker of therapies for their clients.

The app will help the client maintain a history of:

- plan of therapy for client
- therapy already done on client
- therapy to be done on client
- keep track of client appointments
- notify client and therapist of date and time of appointment

## Who’s it for?

The app will be suited for therapists who want to keep track of their clients and the therapy that they do on them.

## Problem Statements

I am a masseuse. I am trying to keep track of my clients. It is difficult to do if I have employees because I do not
know what work has been done on them.

## Goals

- Make an app that keeps a log of client's therapy and their desired outcome of therapy
- Make an app that lets you schedule appointments
- Make an app that lets you notify the client and therapist of the appointment
- Make a web app

## Non Goals
1. At some point make an app that can be viewed on multiple devices. It is currently a test phase, so we should try
   to make it work for the web and then expand, if the need arises.

[//]: # (2. Explain why they are not goals)

[//]: # (3. These are as important and clarifying as the goals)

[//]: # (## Hypothesis)

[//]: # (If we <achieve/enable X>, then <user behavior Y changes in this way> leading to positive metrics Z. Include guesses for size of the win on specific metrics, using past launches as a baseline. )

## Vision Narrative
A small massage business (cca. 5 employees and roughly 25 clients/ week, some reoccurring) wants to digitize it's
logging of therapies for easy access and better time management.
This app will make the therapist's life better, because she will have all her client's history on hand whenever she
needs to check up on it, whether she is on vacation or in the car, she has access to all the newest information with
a click of a button. She does not need to rely on always carrying her log with her everywhere she goes.

## Rough Scoping & Timeline

In V1 there will be:
- login page for therapists
- a basic framework for entering the client's details
- a basic framework for entering the client's therapy sessions

It is a small scale project for now, with a max of 10 therapists and about 25 clients/week.

Tha testing plan is to make a draft version and let it be tested by the client. And later iterate until it is
suitable for her.
Consider the major pieces of functionality, Mobile, Platform,
Internationalization, Entry Points, User Onboarding, Premium.
For the app we need:
- a functioning internet connection
- an authentication login
- authorizations specs
- a database that stores the information of therapies and clients
- a view of previous client history
- a form to fill out about the proposed plan of therapy
- a form for current therapy

## Key Trade Offs & Decisions
**Login: the authentication login approach**
- For now we do the authentication via Google since it is safer and faster to set up.

**Database: a relational DB or document DB?**
- Since it is a simple app and there is not going to be huge data input, we can go for the document DB.

## Concept Mocks
![IMG_7152.png](IMG_7152.png)
![IMG_7153.png](IMG_7153.png)


# Project Proposal

## Proposal
The app has to have these required features:
- **Login page as index page.**
The information we are dealing with is private, so wee need restricted access to it. People who have access are
  employees of the company.

- **Restricted access within the app and transparency**
Every therapist can view each client.
There is an admin and users. *The user* can see all the information from each client, except therapy-specific notes, that are just for a current therapist.
  The notes are private in all aspects.*The ADMIN* has all the access with the task of creating/deleting users.
The app also has an **analytic user** that keeps track of all the analytics and can be shown to investors.

- **Clear visibility** who made what changes to the therapy of a particular client

- **For the first visit** specific information:
  - name and surname
  - email
  - phone number
  - where did the customer find us? # ADMIN
  - why did she choose our salon? # ADMIN
  - is it her first massage in general? # THERAPIST
  - is it her first massage in our salon? # ADMIN
  - how frequently does she visit a massage salon? # ADMIN
  - what does she do for a living (regarding restricted posture)? # THERAPIST

- **Information about client for every visit:**
  - name and surname
  - history of therapy:
    - reason for visiting
    - what does she do for a living (regarding restricted posture)?
    - Therapy plan
    - execution of therapy plan (previous therapies)
    - date of previous visits
    - type of massage (couples, classic, on chair, lymph...)
    - value of massage (coupons for discounts) # ADMIN
  - type of massage
  - value of massage (coupons for discounts) # ADMIN
  - date of current visit
  - name of therapist
  - current therapy (what therapy will be done today)
  - notes on further therapy
  - notes on home therapy for client

- **Search for client** on client page or in archive DB.

- **Retrieve client** from DB archive because she is active again (finished therapy and comes back for a new one at
  a later date)

- **Certain information** from the sign-up form from the website incorporated into the sign-up form (name and
  surname, phone, email)


## Key Features
- login / logout
- input form for new client
- input form for current client
- search database for patient

Login/logout:
- INDEX PAGE has login button that redirects to google login pop up window.
  - Upon success, it automatically redirects to INTRO PAGE

INTRO PAGE:
- displayed therapist's patient's of the day
- view button for patients
- dropdown menu (date, patient)

DISPLAY CURRENT PATIENT:
- name + surname
- occupation
- therapy history (date of previous massage, type of massage, therapy, duration, notes on further therapy/recommendations, personal notes)
- current therapy(type of massage, therapy, duration, notes on further therapy/recommendations, personal notes) # REQUIRED
- submit / edit button

NEW PATIENT:
- name + surname # REQUIRED
- occupation # REQUIRED
- email # REQUIRED
- contact # REQUIRED
- referral
- frequency
- previous massage
- salon_choice
- current therapy(type of massage, therapy, duration, notes on further therapy/recommendations, personal notes) # REQUIRED
- submit / edit button

SEARCH:
- date
- patient

ERROR PAGE:
- error 404gti
- login unsuccessful

DATABASE MODEL:
[data-for-DB.pdf](data-for-DB.pdf)

GENERAL:
- setup DB - MySQL
- integration with Google Auth
- integration with database
- error handling
- deploy settings


For later:
- sms/email notification of future therapy date and time
- calendar
- monthly results from Google analitics


## Key Flows
[Therapy log web app_therapist workflow.pdf](Therapy%20log%20web%20app_therapist%20workflow.pdf)



## Risks & Mitigations


## Open Issues & Key Decisions


[//]: # (## Appendix: Research)
