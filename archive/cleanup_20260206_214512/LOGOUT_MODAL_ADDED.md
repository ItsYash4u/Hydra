# Logout Confirmation Modal - Implemented ✅

## Feature Update
I have added a confirmation popup when a user clicks "Sign Out". This prevents accidental logouts.

## How it Works
1.  **Click Sign Out**: Instead of logging out immediately, a small modal window opens.
2.  **The Modal**:
    - Title: "Sign Out?"
    - Message: "Are you sure you want to sign out of your account?"
    - Icon: Red logout icon.
    - Buttons: "Cancel" (stays logged in) and "Yes, Sign Out" (proceeds to logout).
3.  **After Logout**:
    - You are redirected to the dashboard (or login page/dashboard as guest).
    - The Profile Dropdown will then show "Account" with **Login** and **Sign Up** options.

## Technical Details
- **File**: `greeva/templates/partials/topbar.html`
- **Modal ID**: `#logoutModal`
- **Trigger**: The dropdown item now uses `data-bs-toggle="modal"`.
- **Action**: The "Yes" button carries the original `{% url 'custom_logout' %}` link.

## Verification
1.  **Refresh your browser** (Ctrl+Shift+R).
2.  **Login** (if not already).
3.  **Click Profile Dropdown** > **Sign Out**.
4.  **Verify**: The popup appears.
5.  **Click "Yes, Sign Out"**.
6.  **Verify**: You are logged out, and the dropdown now shows Login/Signup options.

This completes the request for the sign-out popup window! 🚀
