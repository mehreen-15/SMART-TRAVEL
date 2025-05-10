document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Enable tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }

    // Date range picker initialization for trip planning
    const dateRangeInputs = document.querySelectorAll('.date-range-picker');
    if (dateRangeInputs.length > 0) {
        dateRangeInputs.forEach(function(input) {
            // This is a placeholder - you would typically use a library like daterangepicker
            input.addEventListener('click', function() {
                console.log('Date range picker clicked');
            });
        });
    }

    // Star rating handling
    const starRatingInputs = document.querySelectorAll('.star-rating-input');
    if (starRatingInputs.length > 0) {
        starRatingInputs.forEach(function(ratingGroup) {
            const stars = ratingGroup.querySelectorAll('.star');
            const hiddenInput = ratingGroup.querySelector('input[type="hidden"]');
            
            stars.forEach(function(star, index) {
                star.addEventListener('click', function() {
                    const rating = index + 1;
                    hiddenInput.value = rating;
                    
                    // Update visual state
                    stars.forEach(function(s, i) {
                        if (i < rating) {
                            s.classList.add('active');
                        } else {
                            s.classList.remove('active');
                        }
                    });
                });
            });
        });
    }

    // Budget calculator
    const budgetCalculator = document.getElementById('budget-calculator');
    if (budgetCalculator) {
        const calculateBtn = budgetCalculator.querySelector('.calculate-btn');
        calculateBtn.addEventListener('click', function() {
            const accommodationCost = parseFloat(document.getElementById('accommodation-cost').value) || 0;
            const transportationCost = parseFloat(document.getElementById('transportation-cost').value) || 0;
            const foodCost = parseFloat(document.getElementById('food-cost').value) || 0;
            const activitiesCost = parseFloat(document.getElementById('activities-cost').value) || 0;
            const miscCost = parseFloat(document.getElementById('misc-cost').value) || 0;
            
            const totalCost = accommodationCost + transportationCost + foodCost + activitiesCost + miscCost;
            
            document.getElementById('total-budget').textContent = totalCost.toFixed(2);
        });
    }
}); 