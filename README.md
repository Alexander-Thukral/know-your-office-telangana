# Know Your Office — EPFO Telangana Dashboard

A high-performance, standalone search dashboard for Telangana EPFO counter staff to identify establishment offices, provide audio guidance, and generate printable visitor slips.

## 🚀 Features

### 🔍 Smart Search
- **Instant Lookup**: Search by EST ID, PAN, or Establishment Name.
- **Auto-Suggestions**: Responsive search suggestions as you type.
- **Fast Performance**: Handles 150,000+ records in the browser using an optimized JSON index.

### 🎙️ Audio & 🖨️ Print
- **Voice Guidance**: One-click audio announcement of the assigned office (e.g., "Barkatpura").
- **Print Slips**: Professional A4 print slips with:
  - Establishment & Task details.
  - Member Name & validated 22-character Member ID.
  - Grievance category selection.
  - **QR Code**: Embeds all slip details for easy scanning by back-office staff.

### 📋 Visitor Tracking
- **Local Persistence**: Records every visitor interaction in the browser's IndexedDB.
- **Real-time Badge**: Floating "Today's Visitors" counter.
- **History Management**: 
  - View today's log in a clean tabular panel.
  - **Export Today's CSV**: Daily reporting.
  - **Backup ALL History**: Full database export for long-term records.

### 🔒 Admin Panel
- **Secure Updates**: Upload new `TELANGANA_MSTR` CSV files directly via `admin.html`.
- **Robust Processing**: Automatically detects required columns and ignores extra data.
- **GitHub Integration**: Pushes updates directly to the repository (requires a personal access token), triggering automatic Vercel re-deployment.

## 🛠️ Tech Stack
- **Frontend**: HTML5, Vanilla CSS3, JavaScript.
- **Data**: Optimized JSON (pre-processed from CSV).
- **Storage**: IndexedDB (for visitor logs).
- **Deployment**: Vercel / GitHub Pages.

## 📦 Setup & Deployment
1. Clone the repository.
2. Upload to GitHub.
3. Connect the repo to **Vercel** for automatic hosting.
4. Access `/admin.html` to keep your data fresh every month.

---
*Developed for EPFO Telangana Regional Offices.*
