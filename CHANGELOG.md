# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [UNRELEASED]

### Added
- [core] Upgraded material kit from v2.1.1 to v2.2.0
- [core] Upgraded django from v2.2.9 to v2.2.10
- [feedbacks] Introduced an email notification for the authors when a user completes a survey
- [feedbacks] Introduced created and modified dates to answers
- [landing] Introduced 'cards section': a new section template
- [landing] Introduced 'search header': a new featured section template  

### Changed
- [landing] Changed the ordering of search results to make products appear first
- [landing] Updated dashboard visual styles with rounded buttons and card-styled sections
- [product] Added support for the reporting functionality  

### Removed
- [landing] Removed nav dropdowns from navbar

### Fixed

### Security


## [1.0.0-beta.6] → 2019-12-26

### Added
- [ebooks] Introduced replacement rules to better adapt universal sections in any ebook
- [landing] Introduced a new admin page for reporting purposes
- [products] Introduced new actions in products admin page to lock or unlock items
- [products] Introduced related products as new section in product detail page
- [payments] Introduced payments: a new app that handles real money purchases with Stripe services

### Changed
- [accounts] Improved sizing of cards in collection page
- [core] Updated ckeditor config with custom block styles
- [ebooks] Updated table of contents with parts and chapters
- [ebooks] Enabled sections' bookmarks 
- [products] The courtesy message is no longer a mandatory field
- [products] Improved product page mobile responsiveness

### Removed
- [blog] Removed forced uppercase from article's label
- [ebooks] Removed section templates and values

### Fixed
- [ebooks] Fixed a problem that prevented the first section to appear
- [ebooks] Fixed a problem that prevented a chapter image to display

### Security


## [1.0.0-beta.5] → 2019-07-26

### Added
- Introduced sections: a landing model that enables easier customization of the landing page
- Introduced ebooks: a new app that handles the digital content of a product with dynamic chapters, section and search 
- Introduced reviews: a new app that handles reviews for supported content
- Upgraded django to v2.2.3

### Changed
- Enabled a published/draft badge next to publishable content for admin eyes only 
- Improved static files efficiency with deferred loading
- Redesigned product page
- Redesigned blog cards for the landing page

### Removed
- Removed latex requirements since it is now a depreated feature
- Removed the presentatation module since it is now supplanted by sections
- Removed the website logo from error pages
- Removed imgur tags from the admin templates
- Removed unecessary libraries from the comment app

### Fixed
- Fixed a problem that made the product card point to one static page
- Fixed a series of broken links in accounts' templates

### Security
- Upgraded urllib3 to v1.25


## [1.0.0-beta.4] → 2019-03-22

### Added
- Introduced homebrew: an experiental app to write papers
- Introduced feedbacks: an app that automates the creation of surveys
- Introduced a primary link dynamic field that pre-populated with featured objects accross the project
- Upgraded django to v2.1
- Upgraded icons to fontawesome v5.6.3
- Upgrade material kit to v2.1.7

### Changed
- Enabled additional fieldsets for blog admin
- Enabled dynamic cover support for about page
- Enabled blog post preview for admins
- Enabled products section in the landing page
- Updated user report with buttons related to all users, gruped by language
- Updated styles of product carousel
- Updated styles for dropdowns on user page
- Moved about page in the landing page
- Moded authors' profile pictures to imgur

### Removed
- Removed generic feedback form and features
- Removed homebrew app and latex related functionalities

### Fixed
- Fixed an hidden label in the blog admin page
- Fixed a blog hidden field that should be visible
- Fixed a problem that made the survey page crash


## [1.0.0-beta.3] → 2018-06-13

### Added
- Introduced a customization field that lets the user control his favourite language
- Introduced a privacy section that lets the user control and delete its own data
- Introduced a staff-only page that returns all subscribers emails
- Introduced a password reset option in the login modal
- Introduced shortcut links to send emails to subscribers
- Introduced the about page with the summary of our project
- Introduced maintenance mode for published products
- Upgraded the development framework to django 2.1
- Upgraded the icons to fontawesome 5.2

### Changed
- Enabled localization for product files
- Enabled dev folder for development media files
- Enabled asyncronous response to the privacy user form
- Moved articles label to the bottom of the content section
- Moved the feedback button from the navbar to the product page
- Moved secret vars into a secret file in project root 
- Updated fontawesome host from aws to cdn
- Updated error pages 403, 404 and 500 with translations and cleaner layout
- Updated admin list display for users data 
- Enabled translation for users bio

### Fixed
- Fixed a problem that caused user forms to fail badly
- Fixed a problem that made the sign-in form to freeze at the blog page


## [1.0.0-beta.2] → 2018-03-30

### Added
- Introduced users as searchable items
- Introduced parallax effect in the landing, blog and product pages
- Introduced acme utils for https support

### Changed
- Updated material kit pro assets to v2.0.3 with no demo dependances
- Updated navbar background to dark and always fixed to the top
- Updated the feedbackplash message with the username

### Removed
- Removed logo image from the navbar

### Fixed
- Fixed a problem that rendered a wrong width in the blog list page
- Fixed footer positioning in the sign up page 
- Fixed the centering position of the login modal title


## [1.0.0-beta.1] → 2018-02-19

### Added
- Introduced dedicated categories for products and product chapters
- Introduced dynamic cover image for the blog page
- Introduced feedback form in the navbar
- Introduced dynamic image backgrounds for the landing page sections 
- Introduced public rad-only profile page for every user
- Introduced user achievements in the profile page

### Changed
- Updated readme with custom Diventi logo
- Updated article category admin styles
- Updated navbar icons with fontawesome 5 styles
- Updated default button styles from square to round
- Changed image host from S3 to imgur for article and product covers
- Integrated timestamps within the feedback model
- Updated articles layout for mobile devices
- Reformulated main button in the landing page
- Redesigned list of blog cards
- Redesigned product chapter section

### Removed
- Removed sharethis buttons
- Removed label from reply button in the comment section

### Fixed
- Fixed a problem that caused error 500 after pressing the search button with no inputs
- Fixed the anchor links between product and profile pages
- Fixed some translation typos in the profile page
- Fixed a formatting error in user collection page
- Fixed a problem that cut the product image when displayed in small screens
- Adjusted width of product comments
- Deactivated pageheader parallax to prevent html errors
- Fixed DOM errors caused by duplicates ids in the comment section

### Security
- Removed collection urls from the public user page
- Substituded the public link of every product with a temporary link generated on the fly fo the single user


## [1.0.0-alpha.7] → 2018-02-03

### Added
- Introduced threaded comments: comments are now stored as a tree and can be nested.
- Introduced translations: both static or dynamic components may be displayed in english or italian
- Introduced a Vagrantfile to facilitate the development process across different computers
- Introduced sharethis buttons for articles and products
- Added support for sqlite database
- Added uwsgi files for the deployment

### Changed
- Changed to yellow the background color of the inverse navbar links
- Updated important links in the README
- Updated icon styles in the navbar
- Enabled comments count in the blog list page
- Refactored version numbering for pre-releases
- Integrated change password form into profile page

### Fixed
- Fixed minor formatting errors in the changelog
- Fixed layout errors in the base template
- Fixed content cards for product section
- Fixed spacing issues between labels and content cards

### Removed
- Removed page header from search results page
- Removed rich text from landing model fields


## [1.0.0-alpha.6] → 2017-12-30

### Added
- Introduced collections: a centralized space where a user can store any published products
- Introduced a redisegned user profile with new styles, custom avatars and covers 
- Introduced a 5 star rating system for any product 
- Introduced a search engine across products and blog articles accessible from the navbar
- Added search result page that display the title, the description and the contentype for each result
- Added custom 404, 403 and 500 error pages
- Added pageheader to blog list page

### Changed
- Twicked positioning of the header content of the landing page
- Aligned form styles to the yellow theme
- Changed form styles of change password from 'classic' to 'label-floating'
- Unified styles among sign up, sign in and change password pages
- Unified buttons color on blog list, blog detail and product pages
- Refreshed profile page with a new UI inspired by Material Kit
- United user profile and collection in a single page for better anchors
- Set avatar as not required field in profile form
- Disabled promotion bottons for anonymous users
- Integrated the sign in page into a modal
- Updated url conf for update views
- Enabled placeholder for user avatars
- Changed icon of featured product from light hand to solid fire
- Enclosed change password form in a modal
- Hidden section titles if there is no content available in product page
- Enabled placeholder image if the user doesn't have a proper avatar

### Fixed
- Replaced '-' with space on 'signed in/out/up' text occurrences
- Fixed misplaced colors of sign up and sign in buttons
- Fixed fire icon of hot articles
- Adjusted articles right and left margins
- Adjusted uppercase letters in some account forms
- Fixed 500 error page title
- Improved the mobile responsiveness of the account forms
- Enabled comment promotions and preview for any page that uses comments 

### Removed
- Removed attachment support from blogposts (any attachment should be a product)
- Removed timeline assets and data

### Security
- Fixed a problem that a user could expose to update other profiles


## [1.0.0-alpha.5] → 2017-12-09

### Added
- Introduced a profile section on the landing page with a link to the blog page
- Introduced creation and modification dates in blog admin page
- Introduced admin actions to publish and upublish articles
- Introduced a sign up form on the landing page that redirects to the main sign up page
- Introduced a product page to present the featured adventure of the moment
- The product page includes: cover image, details of the document, playable chapters and the story timeline
- Introduced a unique logo on the navbar and favicon
- Introduced a unique logo into the landing page
- Added 'yellow' as a choice to any element in the website
- Added alternative presentation pages for demo purposes
- Added font awesome 5 icons

### Changed
- Avatars are now rendered as urls and uploaded in imgur
- Optimized profile page layout for tables
- Improved responsiveness of the timeline
- Blog's articles pub date is now a datetime field to improve the ordering in blogpost page
- Replaced alien fire of the blog list page with a fire icon
- Replaced nav pills with accordion panels in profile page
- Replaced mini logo with the full logo on the navbar

### Fixed
- Fixed a problem that caused the cov image to disappear
- Fixed user role in profile page
- Fixed a problem that caused the avatar to not be displayed in article page
- Fixed a problem that caused the avatar to not be displayed in comment section
- Fixed a problem that made the background image of blogposts disappear
- Fixed a problem that made the landing page crush if no featured product were found

### Removed
- Removed timeline events from the landing app
- Removed rpg-awesome icons fron the base template


## [1.0.0-alpha.4] → 2017-11-08

### Added
- Introduced avatar grouping to better distinguish those reserved to staff members
- Introduced an animated storyline in the landing page to display a list of main events ordered by date
- Introduced the option to show or hide a staff user on the landing page

### Changed
- Avatar is now optional for user sign-up
- Updated media upload folders to better reflect the app names 
- Reorganized profile page with profile and avatar pillows
- Enabled rich text for page elements
- Updated the description of the storyline section

### Fixed
- Fixed a problem in accounts/widgets that caused an error while migrating the database


## [1.0.0-alpha.3] → 2017-10-29

### Added
- Introduced profile page with avatar, bio and favourite class customization options
- Introduced a dedicated profile picture for staff members
- Introduced detailed profile cards into profile update page

### Changed
- Updated name of comment subpage to better reflect its role
- Hard coded role label for every staff member in the landing page
- Restyled icon addon of sign-up recaptcha to improve its responsiveness
- Succes url of signup changed from landing page to login page

### Fixed
- Fixed a problem that caused double comments in comment section
- Fixed a problem that caused the avatar to be hidden in the landing page
- Fixed a problem that caused the sign-up form to fail silently

### Removed
- Removed automatic login after user signup
- Removed new relic monitoring


## [1.0.0-alpha.2] → 2017-10-20

### Added
- Introduced section "comment preview" under the comment post form
- Introduced navigation for the ordering of comments by promotions or submit date
- Introduced comment toggle button to hide/display all comments

### Changed
- Renamed version.txt to CHANGELOG and adopted Keep a Changelog method for versioning
- Updated README with LICENCE, versioning and incipit infos
- Updated cover visuals in blogposts page

### Fixed
- Fixed a problem that caused the avatar to be a requirement for comment post

### Removed
- Removed icons from navbar


## [1.0.0-alpha.1] → 2017-10-14

### Added
- Introduced a landing page with the presentation of our product
- Introduced a simple accounts management system
- Introduced a blog section
- Introduced a commenting system for the articles
- Introduced a sign-up page with username, email and password 
- Introduced a promotions system for articles and comments
- Introduced an author section on the article page
- Introduced a recaptcha field on the sign-up page