# Schema Design Explination

How to approach making a schema for importing applicant info accross several vendors leaves us with a lot of things to consider.
1. How much do we want to keep the raw data from the vendors (as opposed to having a pipeline draw from and clean but not retain the data)
2. How much do we want to facilitate comparing the data from vendor to vendor?
3. How does versioning matter to our data?

Making some simple assumptions I have created a table in which we have entites, attributes, and keys.
Entities:
* applicants
* applications
* the Orgs that register them

Everything else is considered an attribute of these entiities.

##Summary of main tables:

###Tables created to standardize foreign keys
* Vendor
* Application method
* Organization: This table may be set up differently if the states that organizations work in, the period of time for their funding, and their funding change.

###ALL_RAW:
Every line in this table represents registration information from a given vendor. One to the raw data we add:
* The internal ID we have for that applicant
* The vendor and registration method which is available from the title of the data files.
* The date in which we load this information into our warehouse.

###APPLICATIONS
Each line in this table represents a unique application. So if the same information of an application is represented accross two deferent vendors, here is where they are merged into one line.
In order to build this table we must:
* Understand how vendors standardize information they give us such as name and address, how we standardized that information internally, and how we make it comparable. This will allow us to compare that we are gettting the same info back from vendors about the same applications by the same orgs.
* Understand how we want to codify status, for application methods that require more than one step. This column should yield the most recent step in the process and when it happened.

###Applicant_ID
* This can also be pulled from raw data. It helps record what IDs are given by vendors to which applicants using our internal IDs. This will allow us to compare in consideration to time information from vendors. Should we merge applicants in our unique ID because we determine they are duplicates, this table allows us to record that information accordingly.

###APPLICANT
* Each line in this table should represent a unique applicant.
* If two orgs register a person around the same time, or if someone uses two methods for applying to vote, those inconsistencies should be collapsed systematically into this table.
* Since conflicting applicant data may have different treatments under rules for different states, we have to think through what status we want to give such applicants.
* If two orgs register the same person, we may also think about if we attribute that persons registration to both orgs or two the one who registered that person first.
* This table should allow us to most easily compare the impact organizations and their registration methods.
* Using a codified status column introduced in the applications table also allows us to understand the rate at which organizations address these incomplete applications, if that is of interest.

##Next steps:
* We probably need more than one status column type to fully understand how organizations can address, and pull lists for, folks falling through the cracks in the process.
* We probably want to add tables to fascilitate and track this persons registration status as they move through the system. Especially rejected applications, to aid orgs in addressing them.
