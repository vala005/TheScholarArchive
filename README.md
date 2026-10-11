# The Scholar's Archive — Research Platform

**COMP 3613 Assignment 1 — Individual Report**

The Scholar's Archive is a web-based research platform designed to facilitate the submission, review, and discovery of academic publications. It supports three distinct user roles—Regular Users, Researchers, and Admin Reviewers/Publishers—each with a tailored workflow and dashboard.

## 🚀 Deployed Application

The application is deployed and accessible at:
**[https://thescholararchive.onrender.com/](https://thescholararchive.onrender.com/)**

## ✨ Features & Workflows

The platform is built around three core workflows:

1.  **Search Publications (User):**
    *   Public users can browse the approved publication catalogue without logging in.
    *   Authenticated users gain access to full paper details (including PDF links).
    *   Users can search for papers by title or abstract.
    *   Users can save papers to a personal reading list (Saved Publications).

2.  **Upload Paper (Researcher):**
    *   Authenticated researchers have a dedicated dashboard for managing their submissions.
    *   Researchers can upload new papers by providing a title, abstract, and a PDF file.
    *   Submitted papers enter a "Pending Review" state.
    *   Researchers can view the status of their own submissions (Approved, Rejected, or Pending). If rejected, they can see the deciding admin's identity.

3.  **Review Paper (Admin):**
    *   Admins have a dedicated review queue showing all papers pending review.
    *   Admins can read the paper's details and download the PDF for evaluation.
    *   Admins can approve or reject a paper.
    *   **Approved papers** are published to the public catalogue.
    *   **Rejected papers** remain private to the researcher and the deciding admin.

## 🛠️ Technology Stack

*   **Backend:** Python, Django
*   **Database:** SQLModel / PostgreSQL (via Render)
*   **Frontend:** HTML, CSS (Custom dark-academia theme), JavaScript
*   **Deployment:** Render
*   **Diagrams:** UML (Use Case), Mermaid (Model/ERD)

## 📂 Project Structure
