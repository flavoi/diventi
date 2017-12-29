# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [0.6.3] → 2017-12-29

### Added
- Introduced collections: a centralized space where a user can store any published products
- Introduced a new and redisegned user profile with new styles, custom avatars and covers 
- Introduced a 5 star rating system for any product 
- Introduced a search engine across products and blog articles accessible from the navbar
- Added custom 404, 403 and 500 error pages
- Added pageheader to blog list page
- Added search result page that display the title, the description and the contentype for each result

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

### Removed
- Removed attachment support from blogposts (any attachment should be a product)
- Removed timeline assets and data

### Security
- Fixed a problem that a user could expose to update other profiles


## [0.5.2] → 2017-12-09

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

### Removed
- Removed timeline events from the landing app
- Removed rpg-awesome icons fron the base template


## [0.4.2] → 2017-11-08

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

## Fixed
- Fixed a problem in accounts/widgets that caused an error while migrating the database


## [0.3.3] → 2017-10-29

### Added
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

### Removed
- Removed automatic login after user signup
- Removed new relic monitoring


## [0.2.1] → 2017-10-20

### Added
- Introduced section "comment preview" under the comment post form
- Introduced navigation for the ordering of comments by promotions or submit date
- Introduced comment toggle button to hide/display all comments

### Changed
- Renamed version.txt to CHANGELOG and adopted Keep a Changelog method for versioning
- Updated README with LICENCE, versioning and incipit infos
- Updated cover visuals in blogposts page

### Fixed
- Fixed a problem that caused the avatar to be a requirement for comment post

### Removed
- Removed icons from navbar


## [0.1.0] → 2017-10-14

### Added
- Introduced a landing page with the presentation of our product
- Introduced a simple accounts management system
- Introduced a blog section
- Introduced a commenting system for the articles
- Introduced a sign-up page with username, email and password 
- Introduced a promotions system for articles and comments
- Introduced an author section on the article page
- Introduced a recaptcha field on the sign-up page