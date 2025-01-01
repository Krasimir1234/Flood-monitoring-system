// Fetch user data and populate the profile fields
async function loadUserProfile() {
    try {
        const response = await fetch('/get_user_profile', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const user = await response.json();

            // Populate the fields dynamically
            document.getElementById('nameDisplay').textContent = user.name || 'N/A';
            document.getElementById('emailDisplay').textContent = user.email || 'N/A';
            document.getElementById('usernameDisplay').textContent = user.username || 'N/A';

            document.getElementById('nameInput').value = user.name || '';
            document.getElementById('emailInput').value = user.email || '';
            document.getElementById('usernameInput').value = user.username || '';
        } else {
            console.error('Failed to fetch user data.');
            alert('Unable to load profile data. Please try again later.');
        }
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
}

// Enable profile editing
function editProfile() {
    document.getElementById('nameDisplay').style.display = 'none';
    document.getElementById('emailDisplay').style.display = 'none';
    document.getElementById('usernameDisplay').style.display = 'none';

    document.getElementById('nameInput').style.display = 'inline-block';
    document.getElementById('emailInput').style.display = 'inline-block';
    document.getElementById('usernameInput').style.display = 'inline-block';

    document.getElementById('editBtn').style.display = 'none';
    document.getElementById('saveBtn').style.display = 'inline-block';
}

// Save profile changes
async function saveProfile() {
    const name = document.getElementById('nameInput').value;
    const email = document.getElementById('emailInput').value;
    const username = document.getElementById('usernameInput').value;

    try {
        const response = await fetch('/update_profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, username }),
        });

        const result = await response.json();
        if (result.status === 'success') {
            alert('Profile updated successfully');
            window.location.reload(); // Reload page to reflect changes
        } else {
            alert(result.message || 'Failed to update profile');
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        alert('An error occurred while updating your profile.');
    }
}

// Handle Logout
document.getElementById('logoutButton').addEventListener('click', async function () {
    try {
        const response = await fetch('/logout', { method: 'POST' });
        if (response.ok) {
            alert('Logged out successfully');
            window.location.href = '/login'; // Redirect to login page
        } else {
            console.warn('Logout request failed.');
        }
    } catch (error) {
        console.error('Error during logout:', error);
        alert('An error occurred while logging out.');
    }
});

// Load user profile on page load
document.addEventListener('DOMContentLoaded', loadUserProfile);
