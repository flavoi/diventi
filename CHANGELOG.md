# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased] → xxxx-xx-xx

### Added
- Introduced cover image for product chatpers
- Added search field in the navbar

### Changed
- Twicked positioning of the header content of the landing page

### Fixed
- Replaced '-' with space on 'signed in/out/up' text occurrences
- Fixed misplaced colors of sign up and sign in buttons
- Fixed fire icon of hot articles
- Adjusted articles' right and left margins

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