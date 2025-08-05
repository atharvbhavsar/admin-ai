const translations = {
    // Shared elements like language options
    languages: {
        en: 'English',
        hi: 'हिंदी',
        mr: 'मराठी'
    },
    // Index Page translations
    index: {
        heroTitle: {
            en: 'Find Your Future College, <span class="hero-gradient-text">Instantly.</span>',
            hi: 'अपना भविष्य का कॉलेज खोजें, <span class="hero-gradient-text">तुरंत।</span>',
            mr: 'तुमचे भविष्यातील महाविद्यालय शोधा, <span class="hero-gradient-text">झटपट.</span>'
        },
        heroSubtitle: {
            en: 'Our AI-powered assistant analyzes your profile to recommend the perfect colleges for you after your 12th grade.',
            hi: 'हमारा AI-संचालित सहायक आपकी 12वीं के बाद आपके लिए सही कॉलेजों की सिफारिश करने के लिए आपकी प्रोफ़ाइल का विश्लेषण करता है।',
            mr: 'आमचे AI-चालित सहाय्यक तुमच्या १२वी नंतर तुमच्यासाठी योग्य महाविद्यालयांची शिफारस करण्यासाठी तुमच्या प्रोफाइलचे विश्लेषण करते.'
        },
        heroCTA: { en: 'Start For Free', hi: 'मुफ्त में शुरू करें', mr: 'विनामूल्य प्रारंभ करा' },
        headerGetStarted: { en: 'Get Started', hi: 'शुरू करें', mr: 'सुरु करा' },
        socialProofTitle: { en: 'Trusted by Students from Leading Institutions', hi: 'प्रमुख संस्थानों के छात्रों द्वारा विश्वसनीय', mr: 'प्रमुख संस्थांमधील विद्यार्थ्यांद्वारे विश्वसनीय' },
        features: [
            { icon: '...', title: { en: 'Personalized Recommendations', hi: 'व्यक्तिगत सिफारिशें', mr: 'वैयक्तिकृत शिफारसी' }, desc: { en: 'Get a curated list of colleges based on your marks, interests, and location.', hi: 'अपने अंक, रुचियों और स्थान के आधार पर कॉलेजों की एक क्यूरेटेड सूची प्राप्त करें।', mr: 'तुमचे गुण, आवड आणि स्थानावर आधारित महाविद्यालयांची क्युरेट केलेली यादी मिळवा.' } },
            { icon: '...', title: { en: 'Eligibility Checker', hi: 'पात्रता परीक्षक', mr: 'पात्रता तपासक' }, desc: { en: 'Instantly check if you meet the admission criteria for thousands of courses.', hi: 'हजारों पाठ्यक्रमों के लिए प्रवेश मानदंड पूरा करते हैं या नहीं, तुरंत जांचें।', mr: 'हजारो अभ्यासक्रमांसाठी प्रवेशाचे निकष तुम्ही पूर्ण करता की नाही हे त्वरित तपासा.' } },
            { icon: '...', title: { en: '24/7 AI Counselor', hi: '24/7 एआई काउंसलर', mr: '२४/७ एआय समुपदेशक' }, desc: { en: 'Ask any question about admissions, fees, or deadlines, anytime you want.', hi: 'प्रवेश, शुल्क, या समय सीमा के बारे में कोई भी प्रश्न पूछें, कभी भी।', mr: 'प्रवेश, शुल्क, किंवा अंतिम मुदतीबद्दल कोणताही प्रश्न विचारा, कधीही.' } }
        ],
        testimonials: [
            { quote: { en: "AdmitAI made my college search so easy! I found the perfect engineering college in Pune within a day.", hi: "AdmitAI ने मेरी कॉलेज खोज को इतना आसान बना दिया! मुझे एक दिन के भीतर पुणे में सही इंजीनियरिंग कॉलेज मिल गया।", mr: "AdmitAI ने माझा कॉलेज शोध खूप सोपा केला! मला एका दिवसात पुण्यातील योग्य अभियांत्रिकी महाविद्यालय सापडले." }, name: "Priya S.", rating: 5 },
            { quote: { en: "The eligibility checker is a lifesaver. I knew exactly which colleges I could apply to with my CET score.", hi: "पात्रता परीक्षक एक जीवनरक्षक है। मुझे ठीक-ठीक पता था कि मैं अपने CET स्कोर के साथ किन कॉलेजों में आवेदन कर सकता हूं।", mr: "पात्रता तपासक एक जीवनरक्षक आहे. मला माझ्या CET स्कोरसह कोणत्या महाविद्यालयांमध्ये अर्ज करता येईल हे नक्की माहित होते." }, name: "Amit K.", rating: 5 },
            { quote: { en: "A must-have tool for any 12th-grade student in Maharashtra. Highly recommended!", hi: "महाराष्ट्र में किसी भी 12वीं कक्षा के छात्र के लिए एक आवश्यक उपकरण। अत्यधिक अनुशंसित!", mr: "महाराष्ट्रातील कोणत्याही १२वीच्या विद्यार्थ्यासाठी एक आवश्यक साधन. अत्यंत शिफारसीय आहे!" }, name: "Rohan M.", rating: 5 }
        ],
        faqs: [
            { q: { en: 'Is this service free?', hi: 'क्या यह सेवा मुफ्त है?', mr: 'ही सेवा विनामूल्य आहे का?' }, a: { en: 'Yes, our basic college finder and recommendation service is completely free to use.', hi: 'हाँ, हमारी मूल कॉलेज खोजक और सिफारिश सेवा उपयोग करने के लिए पूरी तरह से मुफ्त है।', mr: 'होय, आमची मूलभूत महाविद्यालय शोधक आणि शिफारस सेवा वापरण्यासाठी पूर्णपणे विनामूल्य आहे.' } },
            { q: { en: 'Which entrance exams do you support?', hi: 'आप कौन सी प्रवेश परीक्षाओं का समर्थन करते हैं?', mr: 'तुम्ही कोणत्या प्रवेश परीक्षांना समर्थन देता?' }, a: { en: 'We support a wide range of exams including MHT-CET, JEE Mains, NEET, and more for accurate recommendations.', hi: 'हम सटीक सिफारिशों के लिए MHT-CET, JEE Mains, NEET, और अधिक सहित कई परीक्षाओं का समर्थन करते हैं।', mr: 'आम्ही अचूक शिफारसींसाठी MHT-CET, JEE Mains, NEET आणि बरेच काही यासह विस्तृत परीक्षांना समर्थन देतो.' } }
        ],
        titles: { features: {en: 'Everything You Need For Your Next Step', hi: 'आपके अगले कदम के लिए सब कुछ', mr: 'तुमच्या पुढच्या पावलासाठी सर्वकाही'}, testimonials: {en:'What Students Say About Us', hi:'छात्र हमारे बारे में क्या कहते हैं', mr:'विद्यार्थी आमच्याबद्दल काय म्हणतात'}, faq: {en: 'Frequently Asked Questions', hi:'अक्सर पूछे जाने वाले प्रश्न', mr:'सतत विचारले जाणारे प्रश्न'}, cta: {en:'Ready to Find Your Dream College?', hi:'क्या आप अपना सपनों का कॉलेज खोजने के लिए तैयार हैं?', mr:'तुमचे स्वप्नातील महाविद्यालय शोधण्यासाठी तयार आहात का?'}},
        subtitles: { features: {en:'Powerful tools designed to simplify your admission journey.', hi:'आपकी प्रवेश यात्रा को सरल बनाने के लिए डिज़ाइन किए गए शक्तिशाली उपकरण।', mr:'तुमचा प्रवेश प्रवास सोपा करण्यासाठी डिझाइन केलेली शक्तिशाली साधने.'}, cta: {en:'Create your free account and get personalized college recommendations in minutes.', hi:'अपना मुफ्त खाता बनाएं और मिनटों में व्यक्तिगत कॉलेज सिफारिशें प्राप्त करें।', mr:'तुमचे विनामूल्य खाते तयार करा आणि काही मिनिटांत वैयक्तिकृत महाविद्यालय शिफारसी मिळवा.'}},
        ctaButton: { en: 'Get My Free Recommendations', hi: 'मेरी मुफ्त सिफारिशें प्राप्त करें', mr: 'माझ्या मोफत शिफारसी मिळवा' }
    },
    // Auth Page translations
    auth: {
        signInTitle: { en: 'Welcome Back!', hi: 'वापस स्वागत है!', mr: 'पुन्हा स्वागत आहे!' },
        signInSubtitle: { en: 'Sign in to continue your journey.', hi: 'अपनी यात्रा जारी रखने के लिए साइन इन करें।', mr: 'तुमचा प्रवास सुरू ठेवण्यासाठी साइन इन करा.' },
        emailLabel: { en: 'Email Address', hi: 'ईमेल पता', mr: 'ईमेल पत्ता' },
        passwordLabel: { en: 'Password', hi: 'पासवर्ड', mr: 'पासवर्ड' },
        signInButton: { en: 'Sign In', hi: 'साइन इन करें', mr: 'साइन इन करा' },
        signInPrompt: { en: "Don't have an account?", hi: 'खाता नहीं है?', mr: 'खाते नाही?' },
        signUpLink: { en: 'Sign Up for free', hi: 'मुफ्त में साइन अप करें', mr: 'विनामूल्य साइन अप करा' },
        signUpTitle1: { en: 'Create Your Account', hi: 'अपना खाता बनाएं', mr: 'तुमचे खाते तयार करा' },
        signUpSubtitle1: { en: 'Step 1: Account Credentials', hi: 'चरण 1: खाता क्रेडेंशियल', mr: 'पायरी 1: खाते क्रेडेंशियल्स' },
        createPasswordLabel: { en: 'Create Password', hi: 'पासवर्ड बनाएं', mr: 'पासवर्ड तयार करा' },
        nextButton: { en: 'Next: Personal Info', hi: 'अगला: व्यक्तिगत जानकारी', mr: 'पुढील: वैयक्तिक माहिती' },
        signUpPrompt: { en: 'Already have an account?', hi: 'पहले से ही एक खाता मौजूद है?', mr: 'आधीपासूनच खाते आहे?' },
        signInLink: { en: 'Sign In', hi: 'साइन इन करें', mr: 'साइन इन करा' },
        signUpTitle2: { en: 'Tell Us About Yourself', hi: 'हमें अपने बारे में बताएं', mr: 'आम्हाला तुमच्याबद्दल सांगा' },
        signUpSubtitle2: { en: 'Step 2: Personal Details', hi: 'चरण 2: व्यक्तिगत विवरण', mr: 'पायरी 2: वैयक्तिक तपशील' },
        nameLabel: { en: 'Full Name', hi: 'पूरा नाम', mr: 'पूर्ण नाव' },
        phoneLabel: { en: 'Mobile Number', hi: 'मोबाइल नंबर', mr: 'मोबाईल नंबर' },
        cityLabel: { en: 'Current City', hi: 'वर्तमान शहर', mr: 'सध्याचे शहर' },
        createAccountButton: { en: 'Create Account & Go to Dashboard', hi: 'खाता बनाएं और डैशबोर्ड पर जाएं', mr: 'खाते तयार करा आणि डॅशबोर्डवर जा' }
    },
    // Dashboard translations
    dashboard: {
        sidebarSubtitle: { en: 'Admission Assistant', hi: 'प्रवेश सहायक', mr: 'प्रवेश सहाय्यक' },
        nav: [
            { id: 'chat', text: { en: 'Chat Assistant', hi: 'चैट सहायक', mr: 'चॅट सहाय्यक' }, active: true },
            { id: 'finder', text: { en: 'Course Finder', hi: 'कोर्स खोजक', mr: 'कोर्स शोधक' }, active: false },
            { id: 'dates', text: { en: 'Important Dates', hi: 'महत्वपूर्ण तिथियां', mr: 'महत्वाच्या तारखा' }, active: false },
            { id: 'status', text: { en: 'Application Status', hi: 'आवेदन स्थिति', mr: 'अर्ज स्थिती' }, active: false },
            { id: 'analytics', text: { en: 'Analytics', hi: 'एनालिटिक्स', mr: 'ॲनालिटिक्स' }, active: false },
            { id: 'settings', text: { en: 'Settings', hi: 'सेटिंग्स', mr: 'सेटिंग्ज' }, active: false },
        ],
        navLogout: { en: 'Logout', hi: 'लॉग आउट', mr: 'लॉग आउट' },
        dashboardTitle: { en: 'AI Admission Assistant', hi: 'एआई प्रवेश सहायक', mr: 'एआय प्रवेश सहाय्यक' },
        welcomeTitle: { en: 'Welcome to AdmitAI! 🎓', hi: 'एडमिटएआई में आपका स्वागत है! 🎓', mr: 'एडमिटएआय मध्ये आपले स्वागत आहे! 🎓' },
        welcomeSubtitle: { en: 'Your intelligent admission assistant is here to help you 24/7', hi: 'आपका बुद्धिमान प्रवेश सहायक 24/7 आपकी मदद करने के लिए यहां है', mr: 'तुमचे बुद्धिमान प्रवेश सहाय्यक तुम्हाला 24/7 मदत करण्यासाठी येथे आहे' },
        cards: [
            { title: { en: 'Find Courses', hi: 'कोर्स खोजें', mr: 'कोर्स शोधा' }, desc: { en: 'Discover programs that match your interests', hi: 'अपनी रुचियों से मेल खाने वाले कार्यक्रम खोजें', mr: 'तुमच्या आवडीनुसार जुळणारे प्रोग्राम शोधा' } },
            { title: { en: 'Check Eligibility', hi: 'पात्रता जांचें', mr: 'पात्रता तपासा' }, desc: { en: 'Verify if you meet admission requirements', hi: 'सत्यापित करें कि क्या आप प्रवेश आवश्यकताओं को पूरा करते हैं', mr: 'तुम्ही प्रवेशाची आवश्यकता पूर्ण करता की नाही हे सत्यापित करा' } },
            { title: { en: 'Important Dates', hi: 'महत्वपूर्ण तिथियां', mr: 'महत्वाच्या तारखा' }, desc: { en: 'Never miss application deadlines', hi: 'आवेदन की समय सीमा कभी न चूकें', mr: 'अर्ज करण्याची अंतिम मुदत कधीही चुकवू नका' } },
            { title: { en: 'Fees & Scholarships', hi: 'शुल्क और छात्रवृत्ति', mr: 'शुल्क आणि शिष्यवृत्ती' }, desc: { en: 'Get financial information and aid options', hi: 'वित्तीय जानकारी और सहायता विकल्प प्राप्त करें', mr: 'आर्थिक माहिती आणि मदत पर्याय मिळवा' } }
        ],
        chatPrompt: { en: "Hi! I'm your AI admission assistant. I can help you with course recommendations, eligibility checks, and more.", hi: 'नमस्ते! मैं आपका एआई प्रवेश सहायक हूं। मैं कोर्स की सिफारिशों, पात्रता जांच, और बहुत कुछ में आपकी मदद कर सकता हूं।', mr: 'नमस्कार! मी तुमचा एआय प्रवेश सहाय्यक आहे. मी कोर्स शिफारसी, पात्रता तपासणी आणि बरेच काही मध्ये तुम्हाला मदत करू शकेन.' },
        status: {
            title: { en: 'System Status', hi: 'सिस्टम स्थिति', mr: 'सिस्टम स्थिती' },
            list: [
                { text: { en: 'AI Assistant Online', hi: 'एआई सहायक ऑनलाइन', mr: 'एआय सहाय्यक ऑनलाइन' }, color: 'green' },
                { text: { en: 'Database Connected', hi: 'डेटाबेस कनेक्टेड', mr: 'डेटाबेस कनेक्टेड' }, color: 'green' },
                { text: { en: 'Human Support Available', hi: 'मानव समर्थन उपलब्ध', mr: 'मानवी समर्थन उपलब्ध' }, color: 'green' }
            ]
        },
        recent: {
            title: { en: 'Recent Queries', hi: 'हाल की पूछताछ', mr: 'अलीकडील प्रश्न' },
            list: [
                { text: { en: 'MBA admission requirements', hi: 'एमबीए प्रवेश आवश्यकताएं', mr: 'एमबीए प्रवेशाची आवश्यकता' }, time: { en: '2 minutes ago', hi: '2 मिनट पहले', mr: '२ मिनिटांपूर्वी' } }
            ]
        },
        stats: {
            title: { en: 'Quick Stats', hi: 'त्वरित आँकड़े', mr: 'द्रुत आकडेवारी' },
            desc: { en: 'Queries Resolved Today', hi: 'आज हल की गई पूछताछ', mr: 'आज निराकरण झालेले प्रश्न' }
        }
    }
};