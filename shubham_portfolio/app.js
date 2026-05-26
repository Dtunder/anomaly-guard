// Tab Switching Logic
const navLinks = document.querySelectorAll('.nav-link');
const tabContents = document.querySelectorAll('.tab-content');

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();

        // Remove active class from all links and tabs
        navLinks.forEach(l => l.classList.remove('active'));
        tabContents.forEach(t => t.classList.remove('active'));

        // Add active class to clicked link and corresponding tab
        link.classList.add('active');
        const targetId = link.getAttribute('href').substring(1);
        document.getElementById(targetId).classList.add('active');

        // Scroll to top smoothly
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});

// Ambient Particle Tracking (Mouse-controlled)
const particleContainer = document.getElementById('particle-container');
const particles = [];
const numParticles = 20;

// Initialize particles
for (let i = 0; i < numParticles; i++) {
    const particle = document.createElement('div');
    particle.classList.add('particle');

    // Random sizes between 50px and 200px
    const size = Math.random() * 150 + 50;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;

    // Random starting positions
    const x = Math.random() * window.innerWidth;
    const y = Math.random() * window.innerHeight;

    // Store data for animation
    particles.push({
        element: particle,
        x: x,
        y: y,
        targetX: x,
        targetY: y,
        speed: Math.random() * 0.05 + 0.01 // Different speeds for depth effect
    });

    particleContainer.appendChild(particle);
}

// Update target positions based on mouse movement
document.addEventListener('mousemove', (e) => {
    const mouseX = e.clientX;
    const mouseY = e.clientY;

    particles.forEach((p, index) => {
        // Create an offset so particles float around the mouse, not directly on it
        const offsetX = (Math.cos(index) * 200);
        const offsetY = (Math.sin(index) * 200);

        p.targetX = mouseX + offsetX;
        p.targetY = mouseY + offsetY;
    });
});

// Animation loop
function animateParticles() {
    particles.forEach(p => {
        // Smoothly interpolate current position to target position
        p.x += (p.targetX - p.x) * p.speed;
        p.y += (p.targetY - p.y) * p.speed;

        // Center the particle on its coordinates
        const rect = p.element.getBoundingClientRect();
        p.element.style.transform = `translate(${p.x - rect.width/2}px, ${p.y - rect.height/2}px)`;
    });

    requestAnimationFrame(animateParticles);
}

animateParticles();

// LOI Generator Logic
function generateLOI(lang) {
    const clientName = document.getElementById('clientName').value;
    const projectDesc = document.getElementById('projectDesc').value;
    const duration = document.getElementById('duration').value;
    const budget = document.getElementById('budget').value;

    if (!clientName || !projectDesc || !duration || !budget) {
        alert(lang === 'de' ? 'Bitte füllen Sie alle Felder aus.' : 'Please fill in all fields.');
        return;
    }

    const date = new Date().toLocaleDateString(lang === 'de' ? 'de-DE' : 'en-US');
    let content = '';

    if (lang === 'de') {
        content = `Absichtserklärung (Letter of Intent)

Datum: ${date}

Hiermit bestätigen wir, ${clientName}, die Absicht, Herrn Shubham Jayswal als freiberuflichen Spezialisten für folgendes Projekt zu beauftragen:

Projektbeschreibung:
${projectDesc}

Voraussichtlicher Umfang / Dauer:
${duration}

Voraussichtliche Vergütung:
${budget}

Diese Absichtserklärung dient zur Vorlage bei der Ausländerbehörde Aachen (gemäß § 21 Abs. 6 AufenthG) zur Beantragung bzw. Genehmigung der selbständigen/freiberuflichen Tätigkeit. Die tatsächliche Beauftragung erfolgt nach Erteilung der entsprechenden Erlaubnis.

Mit freundlichen Grüßen,

___________________________
Unterschrift / Stempel
${clientName}`;
    } else {
        content = `Letter of Intent

Date: ${date}

We, ${clientName}, hereby confirm our intent to contract Mr. Shubham Jayswal as a freelance specialist for the following project:

Project Description:
${projectDesc}

Expected Duration / Scope:
${duration}

Expected Remuneration:
${budget}

This letter of intent is intended for submission to the Foreigners' Registration Office (Ausländerbehörde) in Aachen (pursuant to Section 21 (6) of the Residence Act) to apply for/approve self-employed/freelance activity. The actual contracting will take place upon issuance of the corresponding permit.

Sincerely,

___________________________
Signature / Stamp
${clientName}`;
    }

    document.getElementById('loi-content').textContent = content;
    document.getElementById('loi-result').classList.remove('hidden');

    // Scroll to result
    document.getElementById('loi-result').scrollIntoView({ behavior: 'smooth' });
}

function copyLOI() {
    const content = document.getElementById('loi-content').textContent;
    navigator.clipboard.writeText(content).then(() => {
        const btn = document.querySelector('#loi-result .primary-btn');
        const originalText = btn.textContent;
        btn.textContent = 'Kopiert! / Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        alert('Kopieren fehlgeschlagen. Bitte manuell kopieren.');
    });
}
