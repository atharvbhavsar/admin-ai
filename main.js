document.addEventListener('DOMContentLoaded', () => {
    // ---- GLOBAL LANGUAGE SWITCHER LOGIC ----
    const switcher = document.getElementById('language-switcher');
    let currentLang = localStorage.getItem('language') || 'en';

    // Populate the language switcher options
    if (switcher) {
        Object.keys(translations.languages).forEach(langCode => {
            const option = document.createElement('option');
            option.value = langCode;
            option.textContent = translations.languages[langCode];
            switcher.appendChild(option);
        });
        switcher.value = currentLang; // Set initial value
        switcher.addEventListener('change', (event) => {
            currentLang = event.target.value;
            localStorage.setItem('language', currentLang);
            updatePageText();
        });
    }

    // ---- PAGE-SPECIFIC LOGIC ----
    const pageId = document.body.parentElement.getAttribute('data-page-id');
    
    // --- INDEX PAGE LOGIC ---
    if (document.querySelector('body[data-page-id="index"]')) {
        const updateIndexPageText = () => {
            const elements = translations.index;
            document.getElementById('hero-title').innerHTML = elements.heroTitle[currentLang];
            document.getElementById('hero-subtitle').innerText = elements.heroSubtitle[currentLang];
            document.getElementById('hero-cta').innerText = elements.heroCTA[currentLang];
            document.getElementById('header-get-started').innerText = elements.headerGetStarted[currentLang];
            document.getElementById('social-proof-title').innerText = elements.socialProofTitle[currentLang];
            
            document.querySelector('#features-title').innerText = elements.titles.features[currentLang];
            document.querySelector('#features-subtitle').innerText = elements.subtitles.features[currentLang];
            
            document.querySelector('#testimonials-title').innerText = elements.titles.testimonials[currentLang];
            document.querySelector('#faq-title').innerText = elements.titles.faq[currentLang];
            
            document.querySelector('#cta-title').innerText = elements.titles.cta[currentLang];
            document.querySelector('#cta-subtitle').innerText = elements.subtitles.cta[currentLang];
            document.querySelector('#cta-button').innerText = elements.ctaButton[currentLang];

            const featuresContainer = document.querySelector('.grid');
            featuresContainer.innerHTML = '';
            elements.features.forEach(feature => {
                 featuresContainer.innerHTML += `
                    <div class="feature-card p-8 text-center scroll-animation">
                        <h4 class="text-xl font-semibold text-white mb-2">${feature.title[currentLang]}</h4>
                        <p class="text-gray-400">${feature.desc[currentLang]}</p>
                    </div>`;
            });

            const testimonialsContainer = document.querySelectorAll('.grid')[1];
            testimonialsContainer.innerHTML = '';
            elements.testimonials.forEach(testimonial => {
                testimonialsContainer.innerHTML += `
                    <div class="feature-card p-6 scroll-animation">
                        <p class="text-gray-300 mb-4">"${testimonial.quote[currentLang]}"</p>
                        <p class="font-bold text-white">${testimonial.name}</p>
                    </div>`;
            });
            
            const faqContainer = document.getElementById('faq-container');
            faqContainer.innerHTML = '';
            elements.faqs.forEach(faq => {
                faqContainer.innerHTML += `
                     <div class="faq-item bg-gray-800/50 border border-gray-700 rounded-lg">
                        <button class="faq-question w-full flex justify-between items-center text-left p-4">
                            <span class="font-semibold text-white">${faq.q[currentLang]}</span>
                            <span class="faq-arrow text-white transition-transform">▼</span>
                        </button>
                        <div class="faq-answer px-4 pb-4 text-gray-400">
                           ${faq.a[currentLang]}
                        </div>
                    </div>`;
            });

            // Re-attach FAQ event listeners
            document.querySelectorAll('.faq-question').forEach(button => {
                button.addEventListener('click', () => {
                    button.parentElement.classList.toggle('open');
                });
            });
        };
        
        // Scroll Animations
        const scrollElements = document.querySelectorAll(".scroll-animation");
        const elementInView = (el) => {
            const elementTop = el.getBoundingClientRect().top;
            return elementTop <= (window.innerHeight || document.documentElement.clientHeight);
        };
        const handleScrollAnimation = () => {
            scrollElements.forEach((el) => { if (elementInView(el)) { el.classList.add("animate"); } });
        };
        window.addEventListener("scroll", handleScrollAnimation);
        
        // Initial text set
        updatePageText = updateIndexPageText;
    }

    // --- AUTH PAGE LOGIC ---
    if (document.querySelector('body[data-page-id="auth"]')) {
       const updateAuthPageText = () => {
            const elements = translations.auth;
            document.getElementById('signin-title').innerText = elements.signInTitle[currentLang];
            document.getElementById('signin-subtitle').innerText = elements.signInSubtitle[currentLang];
            document.getElementById('signin-email-label').innerText = elements.emailLabel[currentLang];
            document.getElementById('signin-password-label').innerText = elements.passwordLabel[currentLang];
            document.getElementById('signin-button').innerText = elements.signInButton[currentLang];
            document.getElementById('signin-prompt').innerText = elements.signInPrompt[currentLang];
            document.querySelector('#show-signup-btn').innerText = elements.signUpLink[currentLang];
            
            document.getElementById('signup-title-1').innerText = elements.signUpTitle1[currentLang];
            document.getElementById('signup-subtitle-1').innerText = elements.signUpSubtitle1[currentLang];
            document.getElementById('signup-email-label').innerText = elements.emailLabel[currentLang];
            document.getElementById('signup-password-label').innerText = elements.createPasswordLabel[currentLang];
            document.getElementById('signup-next-btn').innerText = elements.nextButton[currentLang];
            document.getElementById('signup-prompt').innerText = elements.signUpPrompt[currentLang];
            document.querySelector('#show-signin-btn').innerText = elements.signInLink[currentLang];
            document.getElementById('signup-title-2').innerText = elements.signUpTitle2[currentLang];
            document.getElementById('signup-subtitle-2').innerText = elements.signUpSubtitle2[currentLang];
            document.getElementById('signup-name-label').innerText = elements.nameLabel[currentLang];
            document.getElementById('signup-phone-label').innerText = elements.phoneLabel[currentLang];
            document.getElementById('signup-city-label').innerText = elements.cityLabel[currentLang];
            document.getElementById('signup-create-btn').innerText = elements.createAccountButton[currentLang];
       };

        const signInSection = document.getElementById('sign-in-section');
        const signUpSection = document.getElementById('sign-up-section');
        const showSignUpBtn = document.getElementById('show-signup-btn');
        const showSignInBtn = document.getElementById('show-signin-btn');

        showSignUpBtn.addEventListener('click', () => {
            signInSection.classList.remove('active');
            signUpSection.classList.add('active');
        });
        showSignInBtn.addEventListener('click', () => {
            signUpSection.classList.remove('active');
            signInSection.classList.add('active');
        });

        const step1Form = document.getElementById('step1-form');
        const step1Div = document.getElementById('signup-step-1');
        const step2Div = document.getElementById('signup-step-2');

        step1Form.addEventListener('submit', (e) => {
            e.preventDefault();
            step1Div.classList.remove('active');
            step2Div.classList.add('active');
        });
       
        updatePageText = updateAuthPageText;
    }

    // --- DASHBOARD PAGE LOGIC ---
    if (document.querySelector('body[data-page-id="dashboard"]')) {
       const updateDashboardPageText = () => {
            const elements = translations.dashboard;
            document.getElementById('sidebar-subtitle').innerText = elements.sidebarSubtitle[currentLang];
            document.getElementById('nav-logout').innerText = elements.navLogout[currentLang];
            document.getElementById('dashboard-title').innerText = elements.dashboardTitle[currentLang];
            document.getElementById('welcome-title').innerText = elements.welcomeTitle[currentLang];
            document.getElementById('welcome-subtitle').innerText = elements.welcomeSubtitle[currentLang];
            document.getElementById('chat-prompt').innerText = elements.chatPrompt[currentLang];
            document.getElementById('status-title').innerText = elements.status.title[currentLang];
            document.getElementById('recent-title').innerText = elements.recent.title[currentLang];
            document.getElementById('stats-title').innerText = elements.stats.title[currentLang];
            document.getElementById('stats-desc').innerText = elements.stats.desc[currentLang];

            const navContainer = document.getElementById('sidebar-nav');
            navContainer.innerHTML = '';
            elements.nav.forEach(item => {
                navContainer.innerHTML += `<a href="#" class="sidebar-link ${item.active ? 'active text-white' : ''} px-4 py-2.5 rounded-r-lg">${item.text[currentLang]}</a>`;
            });
            
            const cardsContainer = document.getElementById('dashboard-cards');
            cardsContainer.innerHTML = '';
            elements.cards.forEach(card => {
                cardsContainer.innerHTML += `
                    <div class="bg-white p-5 rounded-lg shadow-md text-center">
                        <h4 class="font-bold text-gray-800">${card.title[currentLang]}</h4>
                        <p class="text-sm text-gray-500 mt-1">${card.desc[currentLang]}</p>
                    </div>`;
            });

            const statusContainer = document.getElementById('status-list');
            statusContainer.innerHTML = '';
            elements.status.list.forEach(item => {
                statusContainer.innerHTML += `<p class="text-gray-600"><span class="text-${item.color}-500">●</span> ${item.text[currentLang]}</p>`;
            });

             const recentContainer = document.getElementById('recent-list');
            recentContainer.innerHTML = '';
            elements.recent.list.forEach(item => {
                recentContainer.innerHTML += `<div><p class="text-gray-700">${item.text[currentLang]}</p><p class="text-gray-400">${item.time[currentLang]}</p></div>`;
            });
       };
       updatePageText = updateDashboardPageText;
    }
    
    // Initial call to set text on page load
    if (typeof updatePageText === 'function') {
        updatePageText();
    }
});