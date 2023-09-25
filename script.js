// script.js

document.addEventListener('DOMContentLoaded', function () {
    var locationDropdown = document.getElementById('location-dropdown');
    var stateUtDropdown = document.getElementById('state-ut-dropdown');
    var redirectButton = document.getElementById('redirect-button');
    
    // Define the URLs for states and union territories
    var stateUrls = {
        'Andhra Pradesh': 'https://example.com/andhra_pradesh',
        'Arunachal Pradesh': 'https://arunachalpradeshdashboard.onrender.com',
        'Assam': 'https://example.com/assam',
        'Bihar': 'https://example.com/bihar',
        'Chhattisgarh': 'https://example.com/chhattisgarh',
        'Goa': 'https://goadashboard-2c4s.onrender.com',  
        'Gujarat': 'https://example.com/gujarat',
        'Haryana': 'https://example.com/haryana',
        'Himachal Pradesh': 'https://example.com/himachal_pradesh',
        'Jharkhand': 'https://example.com/jharkhand',
        'Karnataka': 'https://example.com/karnataka',
        'Kerala': 'https://example.com/kerala',
        'Madhya Pradesh': 'https://example.com/madhya_pradesh',
        'Maharashtra': 'https://example.com/maharashtra',
        'Manipur': 'https://example.com/manipur',
        'Meghalaya': 'https://example.com/meghalaya',
        'Mizoram': 'https://example.com/mizoram',
        'Nagaland': 'https://example.com/nagaland',
        'Odisha': 'https://example.com/odisha',
        'Punjab': 'https://example.com/punjab',
        'Rajasthan': 'https://example.com/rajasthan',
        'Sikkim': 'https://example.com/sikkim',
        'Tamil Nadu': 'https://example.com/tamil_nadu',
        'Telangana': 'https://example.com/telangana',
        'Tripura': 'https://example.com/tripura',
        'Uttarakhand': 'https://example.com/uttarakhand',
        'Uttar Pradesh': 'https://example.com/uttar_pradesh',
        'West Bengal': 'https://example.com/west_bengal',
    };

    var utUrls = {
        'Andaman and Nicobar Islands': 'https://example.com/andaman_nicobar_islands',
        'Chandigarh': 'https://example.com/chandigarh',
        'Dadra and Nagar Haveli and Daman & Diu': 'https://example.com/dadra_daman',
        'The Government of NCT of Delhi': 'https://example.com/delhi',
        'Jammu & Kashmir': 'https://example.com/jammu_kashmir',
        'Ladakh': 'https://example.com/ladakh',
        'Lakshadweep': 'https://example.com/lakshadweep',
        'Puducherry': 'https://example.com/puducherry',
    };

    locationDropdown.addEventListener('change', function () {
        var locationType = locationDropdown.value;
        stateUtDropdown.innerHTML = ''; // Clear existing options

        if (locationType === 'states') {
            var stateOptions = Object.keys(stateUrls);
        } else if (locationType === 'ut') {
            var stateOptions = Object.keys(utUrls);
        }

        stateOptions.forEach(function (state) {
            var newOption = document.createElement('option');
            newOption.text = state;
            newOption.value = state;
            stateUtDropdown.appendChild(newOption);
        });
    });

    redirectButton.addEventListener('click', function () {
        var selectedLocation = stateUtDropdown.value;
        var selectedUrl = '';

        if (locationDropdown.value === 'states') {
            selectedUrl = stateUrls[selectedLocation];
        } else if (locationDropdown.value === 'ut') {
            selectedUrl = utUrls[selectedLocation];
        }

        if (selectedUrl) {
            window.open(selectedUrl, '_blank'); // Open the selected URL in a new tab
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // Add the "active" class to trigger the animation
    const aboutElements = document.querySelectorAll(".about-animation");
    aboutElements.forEach((element) => {
        element.classList.add("active");
    });
});
