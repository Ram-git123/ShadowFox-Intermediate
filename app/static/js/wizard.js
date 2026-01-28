// your code goes here
function nextStep(step) {
    // Hide all steps with a fade-out effect
    const steps = document.querySelectorAll('.step');
    steps.forEach(s => {
        s.style.display = 'none';
        s.classList.remove('animate__fadeInRight');
    });

    // Show current step with bounce/fade effect
    const target = document.getElementById('step' + step);
    target.style.display = 'block';
    target.classList.add('animate__fadeInRight');

    // Update Progress
    const progress = (step / 3) * 100;
    document.getElementById('progress-bar').style.width = progress + '%';
    document.getElementById('step-indicator').innerText = `Step ${step} of 3`;
}