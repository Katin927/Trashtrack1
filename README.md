TrashTrack 🌿

Trashtrack URL: https://trashtrack1-2bb65cc65e3d.herokuapp.com/
Github repo URL: https://github.com/Katin927/Trashtrack1 
Project Initial Ideas: https://docs.google.com/document/d/1Bv1ZbBIUO3S3tgEqCH02lJJlElAWuz1TXBgoG-UsJSg/edit?usp=sharing 
Project Proposal: https://docs.google.com/document/d/1Ws2wytxmnglUyyrCsaHHWI3DbmTitoWOKAfWItZMbOY/edit?usp=sharing 


What is TrashTrack?

TrashTrack is a web-based application that helps users track, classify, and log their waste in order to build more sustainable recycling habits. Users can quickly scan a barcode or manually enter item details to receive recycling guidance, log their waste history, and visualize their environmental impact.

Features Implemented

Barcode Scanning: Live barcode scanning using QuaggaJS to quickly identify products.

Manual Waste Entry: Users can manually enter items when barcode scanning is not available.

Automatic Waste Classification: Waste items are classified into categories like Plastic, Metal, Glass, Paper, or Other based on barcode data.

Personalized Recycling Tips: Based on item category, users receive advice on proper disposal.

Waste Logging: Users can log waste items and view them in their history.

Dashboard with Analytics: Visualize waste breakdowns via charts, view recent history, and get recycling tips.

Light/Dark Mode Toggle: Users can switch between light and dark dashboard themes.

Authentication: Secure signup and login functionality using Flask-Login.

Toast Notifications: Confirm successful waste logging with dynamic messages.

Why These Features?

The goal was to build an easy-to-use tool that motivates sustainable habits through instant feedback and simple logging. Barcode scanning removes friction from waste tracking. Dashboards and tips educate users about proper recycling methods, making environmental action easy and engaging.

Standard User Flow

User signs up and logs into TrashTrack.

User either scans a barcode using the live camera or manually enters an item.

TrashTrack looks up the barcode, classifies the item into a recycling category, and displays proper disposal advice.

User logs the item, and it appears in their waste history.

User views analytics on the dashboard to see waste breakdowns over time.

APIs Used

OpenFoodFacts API: Provides product information and packaging details based on barcodes.

Earth911 API: Provides material classification data for recycling recommendations.

Technology Stack

Frontend: HTML5, CSS3, Bootstrap 5, JavaScript (vanilla), QuaggaJS (barcode scanning)

Backend: Python, Flask, Flask-Login, Flask-Migrate

Database: PostgreSQL (hosted on Heroku)

Deployment: Heroku

Templating: Jinja2

Future Improvements

Google Vision API: Integrate image-based item classification for items without barcodes.

Google Maps API: Help users find nearby recycling centers based on location and item type.

OpenAI API: Generate AI-powered personalized sustainability tips and waste reduction recommendations.

Gamification Features: Introduce challenges, leaderboards, and rewards for sustainable waste habits.

Business Waste Management Dashboard: Add analytics and compliance tracking for organizations and municipalities.

Additional Notes

TrashTrack currently focuses on core waste tracking and user analytics.

Future updates will focus on expanding AI capabilities, mobile optimization, and gamification to increase engagement.

Challenges during development included ensuring reliable barcode detection and managing differences between development and production database schemas.

Project Planning Files

Initial Project Ideas: Uploaded to GitHub repository.

Project Proposal Template: Uploaded to GitHub repository.

🚀 Deployment

Deployed via Heroku.
Please view the live application to experience barcode scanning, waste logging, and dashboard insights.

Thank You!

TrashTrack was built to make sustainable waste management easy, educational, and impactful. Let's track smarter, recycle better, and protect the Earth together! 
