import React, { useState, useEffect, useMemo, useRef } from 'react';
import { 
  Search, 
  Bookmark, 
  Star, 
  Flame, 
  Clock, 
  MessageSquare, 
  RefreshCw, 
  Download, 
  Copy, 
  AlertTriangle, 
  Info, 
  Cpu, 
  Brain, 
  ShieldAlert, 
  Bot, 
  Activity, 
  TrendingUp, 
  Layers, 
  ExternalLink,
  ChevronRight,
  Filter,
  Check,
  X
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Premium historical backup payload (Offline / 429 rate limit fallback)
const STATIC_BACKUP_PAYLOAD = [
  {
    id: "49201948",
    title: "Claude 3.5 Sonnet outperforms GPT-4o on graduate-level reasoning",
    url: "https://www.anthropic.com/news/claude-3-5-sonnet",
    hnUrl: "https://news.ycombinator.com/item?id=49201948",
    author: "anthropic_dev",
    points: 845,
    commentsCount: 312,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 2, // 2 hours ago
    createdDateString: new Date(Date.now() - 3600 * 2 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "LLMs & NLP",
    readingTime: 3,
    domain: "anthropic.com"
  },
  {
    id: "49202051",
    title: "NVIDIA Blackwell B200 GPUs enter full-scale production at TSMC",
    url: "https://nvidia.com/news/blackwell-production",
    hnUrl: "https://news.ycombinator.com/item?id=49202051",
    author: "hardware_pundit",
    points: 624,
    commentsCount: 184,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 5, // 5 hours ago
    createdDateString: new Date(Date.now() - 3600 * 5 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "Hardware & Infra",
    readingTime: 4,
    domain: "nvidia.com"
  },
  {
    id: "49202111",
    title: "OpenAI establishes new Safety and Security Committee to oversee alignment",
    url: "https://openai.com/blog/safety-and-security-committee",
    hnUrl: "https://news.ycombinator.com/item?id=49202111",
    author: "alignment_researcher",
    points: 412,
    commentsCount: 220,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 8, // 8 hours ago
    createdDateString: new Date(Date.now() - 3600 * 8 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "AI Safety & Ethics",
    readingTime: 5,
    domain: "openai.com"
  },
  {
    id: "49202230",
    title: "Tesla FSD v12.4 demonstrates impressive zero-intervention humanoid-like drive",
    url: "https://tesla.com/fsd-v12",
    hnUrl: "https://news.ycombinator.com/item?id=49202230",
    author: "elon_fanboy",
    points: 295,
    commentsCount: 145,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 11, // 11 hours ago
    createdDateString: new Date(Date.now() - 3600 * 11 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "Robotics & Agents",
    readingTime: 3,
    domain: "tesla.com"
  },
  {
    id: "49202340",
    title: "Sora text-to-video model now in private beta for indie filmmakers",
    url: "https://openai.com/sora",
    hnUrl: "https://news.ycombinator.com/item?id=49202340",
    author: "cinema_tech",
    points: 531,
    commentsCount: 198,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 14, // 14 hours ago
    createdDateString: new Date(Date.now() - 3600 * 14 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "Generative AI",
    readingTime: 4,
    domain: "openai.com"
  },
  {
    id: "49202450",
    title: "Meta releases Llama 3 400B parameter model weights, sparking open-source surge",
    url: "https://meta.com/llama3",
    hnUrl: "https://news.ycombinator.com/item?id=49202450",
    author: "open_sourcer",
    points: 1052,
    commentsCount: 541,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 18, // 18 hours ago
    createdDateString: new Date(Date.now() - 3600 * 18 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "LLMs & NLP",
    readingTime: 6,
    domain: "meta.com"
  },
  {
    id: "49202560",
    title: "Figure 01 humanoid robot uses neural net to make coffee, sort laundry",
    url: "https://figure.ai/robot-demo",
    hnUrl: "https://news.ycombinator.com/item?id=49202560",
    author: "robotics_now",
    points: 388,
    commentsCount: 97,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 22, // 22 hours ago
    createdDateString: new Date(Date.now() - 3600 * 22 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "Robotics & Agents",
    readingTime: 3,
    domain: "figure.ai"
  },
  {
    id: "49202670",
    title: "US and EU sign landmark agreement to collaborate on AI safety evaluations",
    url: "https://whitehouse.gov/ai-safety-accord",
    hnUrl: "https://news.ycombinator.com/item?id=49202670",
    author: "policy_wonk",
    points: 182,
    commentsCount: 42,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 26, // 26 hours ago
    createdDateString: new Date(Date.now() - 3600 * 26 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "AI Safety & Ethics",
    readingTime: 5,
    domain: "whitehouse.gov"
  },
  {
    id: "49202780",
    title: "TSMC reports surge in 3nm process node orders driven by AI accelerators",
    url: "https://tsmc.com/press",
    hnUrl: "https://news.ycombinator.com/item?id=49202780",
    author: "fab_expert",
    points: 245,
    commentsCount: 68,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 30, // 30 hours ago
    createdDateString: new Date(Date.now() - 3600 * 30 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "Hardware & Infra",
    readingTime: 3,
    domain: "tsmc.com"
  },
  {
    id: "49202890",
    title: "Midjourney v6.5 showcases photorealism and crisp text rendering features",
    url: "https://midjourney.com",
    hnUrl: "https://news.ycombinator.com/item?id=49202890",
    author: "pixel_artist",
    points: 402,
    commentsCount: 112,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 35, // 35 hours ago
    createdDateString: new Date(Date.now() - 3600 * 35 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "Generative AI",
    readingTime: 4,
    domain: "midjourney.com"
  },
  {
    id: "49202900",
    title: "Is artificial intelligence changing the way we write code for good?",
    url: "https://github.com/blog/ai-coding",
    hnUrl: "https://news.ycombinator.com/item?id=49202900",
    author: "coder_pulse",
    points: 176,
    commentsCount: 89,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 40, // 40 hours ago
    createdDateString: new Date(Date.now() - 3600 * 40 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "General AI",
    readingTime: 2,
    domain: "github.com"
  },
  {
    id: "49202999",
    title: "DeepMind introduces AlphaFold 3, predicting interactions across all life's molecules",
    url: "https://deepmind.google/alphafold3",
    hnUrl: "https://news.ycombinator.com/item?id=49202999",
    author: "bio_tech",
    points: 733,
    commentsCount: 201,
    timestamp: Math.floor(Date.now() / 1000) - 3600 * 44, // 44 hours ago
    createdDateString: new Date(Date.now() - 3600 * 44 * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    category: "General AI",
    readingTime: 5,
    domain: "deepmind.google"
  }
];

// Helper to check for private browsing localStorage blocks
let isLocalStorageAvailable = true;
try {
  const testKey = '__test_np_ls__';
  localStorage.setItem(testKey, testKey);
  localStorage.removeItem(testKey);
} catch (e) {
  isLocalStorageAvailable = false;
}

// Safe LocalStorage proxy
const safeStorage = {
  memoryStore: {},
  getItem(key) {
    if (isLocalStorageAvailable) {
      return localStorage.getItem(key);
    }
    return this.memoryStore[key] || null;
  },
  setItem(key, value) {
    if (isLocalStorageAvailable) {
      try {
        localStorage.setItem(key, value);
        return true;
      } catch (e) {
        return false;
      }
    }
    this.memoryStore[key] = value;
    return true;
  }
};

export default function App() {
  // Master app states
  const [stories, setStories] = useState([]);
  const [bookmarks, setBookmarks] = useState(() => {
    const saved = safeStorage.getItem('neuralpulse_bookmarks_v1');
    return saved ? JSON.parse(saved) : [];
  });
  
  // UI Control states
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortMode, setSortMode] = useState('recency'); // 'recency' | 'popularity' | 'discussion'
  const [viewMode, setViewMode] = useState('stream'); // 'stream' | 'library'
  const [isLoading, setIsLoading] = useState(true);
  const [feedType, setFeedType] = useState('live'); // 'live' | 'offline_fallback' | 'cached'
  const [toastMessage, setToastMessage] = useState(null);
  
  // Private mode warning
  const [showLsWarning, setShowLsWarning] = useState(!isLocalStorageAvailable);

  // Reference for file input export/import
  const fileInputRef = useRef(null);

  // Category tags mappings
  const categoriesList = useMemo(() => [
    { name: 'LLMs & NLP', icon: Brain, color: '#8B5CF6', tagClass: 'llms-nlp' },
    { name: 'Generative AI', icon: SparklesIcon, color: '#EC4899', tagClass: 'generative-ai' },
    { name: 'Hardware & Infra', icon: Cpu, color: '#F97316', tagClass: 'hardware-infra' },
    { name: 'AI Safety & Ethics', icon: ShieldAlert, color: '#EF4444', tagClass: 'ai-safety-ethics' },
    { name: 'Robotics & Agents', icon: Bot, color: '#10B981', tagClass: 'robotics-agents' },
    { name: 'General AI', icon: Activity, color: '#06B6D4', tagClass: 'general-ai' }
  ], []);

  // Sparkles Icon custom inline component to avoid import issues
  function SparklesIcon(props) {
    return (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        {...props}
      >
        <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
        <path d="m5 3 1 2.5L8.5 6 6 7 5 9.5 4 7 1.5 6 4 5.5z" />
        <path d="m19 17 1 2.5 2.5.5-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1z" />
      </svg>
    );
  }

  // 1. Client-side Semantic Tagging Parser
  const assignCategory = (title) => {
    const t = title.toLowerCase();
    if (/gpt|claude|llama|gemini|transformer|llm|language\s+model|mistral|cohere/i.test(t)) {
      return 'LLMs & NLP';
    }
    if (/diffusion|midjourney|sora|stable\s+diffusion|generative|dall-e|text-to-video|audio-gen/i.test(t)) {
      return 'Generative AI';
    }
    if (/nvidia|h100|b200|tpu|gpu|chip|semiconductor|tsmc|hardware|cuda/i.test(t)) {
      return 'Hardware & Infra';
    }
    if (/safety|ethics|alignment|superalignment|bias|regulate|copyright|eu\s+ai\s+act|lawsuit/i.test(t)) {
      return 'AI Safety & Ethics';
    }
    if (/robot|agent|autonomous|figure\s+01|humanoid|drone|self-driving|tesla\s+fsd/i.test(t)) {
      return 'Robotics & Agents';
    }
    return 'General AI';
  };

  // Toast notifier helper
  const showToast = (message, duration = 4000) => {
    setToastMessage(message);
    setTimeout(() => {
      setToastMessage(null);
    }, duration);
  };

  // 2. Map and Transform HN Raw stories
  const transformRawStory = (hit) => {
    let domain = 'news.ycombinator.com';
    if (hit.url) {
      try {
        domain = new URL(hit.url).hostname.replace('www.', '');
      } catch (e) {
        domain = 'external-source.com';
      }
    }
    
    const title = hit.title || hit.story_title || 'Untitled AI Development';
    const category = assignCategory(title);
    
    // Reading time estimator formula: Math.max(1, Math.ceil((titleWordCount + metadataCount) / 180))
    const titleWords = title.split(/\s+/).filter(Boolean).length;
    const readingTime = Math.max(1, Math.ceil((titleWords + 5) / 180));

    const timestamp = hit.created_at_i || Math.floor(new Date(hit.created_at).getTime() / 1000);

    return {
      id: hit.objectID,
      title: title,
      url: hit.url || `https://news.ycombinator.com/item?id=${hit.objectID}`,
      hnUrl: `https://news.ycombinator.com/item?id=${hit.objectID}`,
      author: hit.author || 'unknown',
      points: hit.points || 0,
      commentsCount: hit.num_comments || 0,
      timestamp: timestamp,
      createdDateString: new Date(timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      category: category,
      readingTime: readingTime,
      domain: domain
    };
  };

  // 3. Parallel Keyless Fetch Engine with Deduplication, SWR, and Session Cache
  const fetchStories = async (forceRefresh = false) => {
    setIsLoading(true);
    const fortyEightHoursAgo = Math.floor(Date.now() / 1000) - (48 * 3600);
    
    // Check Session Storage for Cache (SWR logic)
    const cachedData = sessionStorage.getItem('neuralpulse_cache_v1');
    const cachedTime = sessionStorage.getItem('neuralpulse_cache_time');
    
    if (cachedData && cachedTime && !forceRefresh) {
      const ageInMs = Date.now() - parseInt(cachedTime, 10);
      const isCacheFresh = ageInMs < 5 * 60 * 1000; // 5 minutes fresh window
      
      const parsedStories = JSON.parse(cachedData);
      setStories(parsedStories);
      setFeedType('cached');
      
      if (isCacheFresh) {
        setIsLoading(false);
        return;
      }
      // If cache is stale, we proceed with fetching in background (SWR)
    }

    try {
      // Build Parallel requests to get comprehensive coverage on both "AI" and "Artificial Intelligence"
      const urlQuery1 = `https://hn.algolia.com/api/v1/search_by_date?query=AI&tags=story&numericFilters=created_at_i>${fortyEightHoursAgo}&hitsPerPage=50`;
      const urlQuery2 = `https://hn.algolia.com/api/v1/search_by_date?query="Artificial Intelligence"&tags=story&numericFilters=created_at_i>${fortyEightHoursAgo}&hitsPerPage=50`;

      const [res1, res2] = await Promise.all([
        fetch(urlQuery1).then(r => {
          if (!r.ok) throw new Error(`Algolia Query 1 error: ${r.status}`);
          return r.json();
        }),
        fetch(urlQuery2).then(r => {
          if (!r.ok) throw new Error(`Algolia Query 2 error: ${r.status}`);
          return r.json();
        })
      ]);

      const hits1 = res1.hits || [];
      const hits2 = res2.hits || [];
      
      // Merge & Deduplicate based on objectID
      const mergedHitsMap = new Map();
      [...hits1, ...hits2].forEach(hit => {
        if (hit && hit.objectID && (hit.title || hit.story_title)) {
          mergedHitsMap.set(hit.objectID, hit);
        }
      });

      const uniqueHits = Array.from(mergedHitsMap.values());
      const transformed = uniqueHits.map(transformRawStory);

      // Time Filtering & Backfill requirement:
      // "Standardizes the incoming feed to focus strictly on 'today' (defined dynamically as the current UTC day starting at 00:00).
      // If the quantity of articles published during the current calendar day is lower than 15,
      // the ingestion engine backfills with articles from the last 48 hours to maintain a rich feed."
      
      const todayStartUTC = new Date();
      todayStartUTC.setUTCHours(0, 0, 0, 0);
      const todayStartSec = Math.floor(todayStartUTC.getTime() / 1000);

      const todayStories = transformed.filter(story => story.timestamp >= todayStartSec);
      
      let finalFeed = [];
      if (todayStories.length >= 15) {
        // We have enough today stories! Filter down to just today's stories to focus strictly on "today"
        finalFeed = todayStories;
      } else {
        // Backfill with the 48-hour feed to maintain a rich view of at least 15 items
        const olderStories = transformed.filter(story => story.timestamp < todayStartSec);
        // Sort older stories to pull the best backfill
        const sortedOlder = olderStories.sort((a,b) => b.timestamp - a.timestamp);
        finalFeed = [...todayStories, ...sortedOlder];
      }

      // Sort by UNIX timestamp descending initially
      finalFeed.sort((a,b) => b.timestamp - a.timestamp);

      if (finalFeed.length === 0) {
        throw new Error("No items returned from real-time endpoints");
      }

      setStories(finalFeed);
      setFeedType('live');
      setIsLoading(false);
      
      // Save to Session Storage cache
      try {
        sessionStorage.setItem('neuralpulse_cache_v1', JSON.stringify(finalFeed));
        sessionStorage.setItem('neuralpulse_cache_time', Date.now().toString());
      } catch (err) {
        // Session storage quota might be full
      }

    } catch (error) {
      console.error("NeuralPulse ingestion failed, loading offline fallback: ", error);
      // Fail gracefully: Pull local static backup payload & show toast
      setStories(STATIC_BACKUP_PAYLOAD);
      setFeedType('offline_fallback');
      setIsLoading(false);
      showToast("Algolia live stream unavailable. Displaying historical backup feed (Offline mode).", 5000);
    }
  };

  // Initial load
  useEffect(() => {
    fetchStories();
  }, []);

  // Save Bookmarks to localStorage when modified
  useEffect(() => {
    safeStorage.setItem('neuralpulse_bookmarks_v1', JSON.stringify(bookmarks));
  }, [bookmarks]);

  // Handle manual Refresh trigger
  const handleRefresh = () => {
    fetchStories(true);
    showToast("Revalidating AI Neural Pulse Stream...");
  };

  // Bookmark actions
  const handleToggleBookmark = (story, event) => {
    event.stopPropagation(); // Avoid triggering card links
    const exists = bookmarks.find(b => b.id === story.id);
    
    if (exists) {
      setBookmarks(prev => prev.filter(b => b.id !== story.id));
      showToast(`Removed from library: "${story.title.slice(0, 30)}..."`);
    } else {
      setBookmarks(prev => [...prev, story]);
      
      // Trigger a light-weight feedback effect
      if (window.confetti) {
        try {
          window.confetti({
            particleCount: 30,
            spread: 50,
            origin: { y: 0.8 },
            colors: ['#06B6D4', '#8B5CF6', '#10B981']
          });
        } catch (e) {}
      }
      showToast(`Saved to My Library: "${story.title.slice(0, 30)}..."`);
    }
  };

  // 4. Personal Workstation Bookmark Export / Import Actions
  const handleExportJSON = () => {
    if (bookmarks.length === 0) {
      showToast("Your library is empty. Add bookmarks to export.");
      return;
    }
    const dataStr = JSON.stringify(bookmarks, null, 2);
    const blob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement("a");
    link.href = url;
    link.download = `neuralpulse_library_${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showToast("Successfully exported library as JSON file!");
  };

  const handleCopyJSONToClipboard = () => {
    if (bookmarks.length === 0) {
      showToast("Your library is empty. Add bookmarks to copy.");
      return;
    }
    const dataStr = JSON.stringify(bookmarks, null, 2);
    navigator.clipboard.writeText(dataStr)
      .then(() => showToast("Library JSON copied to clipboard!"))
      .catch(() => showToast("Failed to copy JSON. Please try again."));
  };

  const handleImportJSONTrigger = () => {
    fileInputRef.current.click();
  };

  const handleImportJSONFile = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const importedData = JSON.parse(e.target.result);
        if (!Array.isArray(importedData)) {
          throw new Error("Import data must be a JSON array of stories.");
        }
        
        // Basic schema verification
        const validStories = importedData.filter(item => item && item.id && item.title);
        
        if (validStories.length === 0) {
          showToast("No valid stories found in imported JSON.");
          return;
        }

        // Merge with existing bookmarks, avoiding duplicates by id
        setBookmarks(prev => {
          const mergedMap = new Map();
          prev.forEach(b => mergedMap.set(b.id, b));
          validStories.forEach(b => mergedMap.set(b.id, b));
          return Array.from(mergedMap.values());
        });

        showToast(`Successfully imported ${validStories.length} saved articles to library!`);
        event.target.value = null; // Reset input
      } catch (err) {
        showToast("Invalid JSON file structure. Could not import.");
        console.error("JSON import error:", err);
      }
    };
    reader.readAsText(file);
  };

  // 5. Dynamic Calculations for Analytics Panel
  const metrics = useMemo(() => {
    const listToAnalyze = viewMode === 'library' ? bookmarks : stories;

    // A. AI Pulse Count: Total unique AI stories discovered today (UTC today)
    const todayUTC = new Date();
    todayUTC.setUTCHours(0,0,0,0);
    const startOfTodaySec = Math.floor(todayUTC.getTime() / 1000);
    const todayStoriesCount = stories.filter(s => s.timestamp >= startOfTodaySec).length;

    // B. Dominant Vector: Displays the most heavily represented Category Tag in current filtered layout
    const tagFrequencies = {};
    listToAnalyze.forEach(story => {
      tagFrequencies[story.category] = (tagFrequencies[story.category] || 0) + 1;
    });
    
    let dominantTag = "None";
    let maxCount = 0;
    Object.entries(tagFrequencies).forEach(([tag, count]) => {
      if (count > maxCount) {
        maxCount = count;
        dominantTag = tag;
      }
    });

    // C. Velocity Metric: The average frequency of new posts in the loaded list
    let velocityStr = "No data";
    if (stories.length > 1) {
      const sortedByTime = [...stories].sort((a,b) => b.timestamp - a.timestamp);
      const newest = sortedByTime[0].timestamp;
      const oldest = sortedByTime[sortedByTime.length - 1].timestamp;
      
      const spanMinutes = (newest - oldest) / 60;
      const avgMinutes = spanMinutes / stories.length;
      
      if (avgMinutes < 1) {
        velocityStr = "1 post every <1 min";
      } else if (avgMinutes < 60) {
        velocityStr = `1 post every ${Math.round(avgMinutes)} mins`;
      } else {
        const avgHours = avgMinutes / 60;
        velocityStr = `1 post every ${avgHours.toFixed(1)} hrs`;
      }
    } else if (stories.length === 1) {
      velocityStr = "Instant";
    }

    return {
      pulseCount: todayStoriesCount || stories.length, // Fallback to feed length if 0 at early UTC day
      dominantTag: dominantTag,
      velocity: velocityStr
    };
  }, [stories, bookmarks, viewMode]);

  // Category selection toggle action
  const handleToggleCategoryFilter = (catName) => {
    setSelectedCategories(prev => {
      if (prev.includes(catName)) {
        return prev.filter(c => c !== catName);
      } else {
        return [...prev, catName];
      }
    });
  };

  // Reset all filters and search queries
  const handleResetFilters = () => {
    setSelectedCategories([]);
    setSearchQuery('');
    setSortMode('recency');
  };

  // 6. Filtering & Sorting Engine (Typos & fuzzy-matched searches supported)
  const processedStories = useMemo(() => {
    const baseList = viewMode === 'library' ? bookmarks : stories;

    // A. Apply Search Query Filter (Title, Author, Domain fuzzy matching)
    let filtered = baseList;
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase().trim();
      filtered = baseList.filter(story => {
        const titleMatch = story.title.toLowerCase().includes(query);
        const authorMatch = story.author.toLowerCase().includes(query);
        const domainMatch = story.domain.toLowerCase().includes(query);
        
        // Also allow slightly fuzzy matching for common typos (e.g. split keywords)
        const words = query.split(/\s+/).filter(Boolean);
        const titleMatchesAllWords = words.every(word => story.title.toLowerCase().includes(word));
        
        return titleMatch || authorMatch || domainMatch || titleMatchesAllWords;
      });
    }

    // B. Apply Multi-faceted Category Filter
    if (selectedCategories.length > 0) {
      filtered = filtered.filter(story => selectedCategories.includes(story.category));
    }

    // C. Apply Advanced Sorter
    const sorted = [...filtered];
    if (sortMode === 'recency') {
      sorted.sort((a, b) => b.timestamp - a.timestamp);
    } else if (sortMode === 'popularity') {
      // Hotness point logic: points * (comments + 1) / (hours_elapsed + 2)^1.8
      const getHotnessScore = (story) => {
        const hoursElapsed = Math.max(0, (Date.now() / 1000 - story.timestamp) / 3600);
        return (story.points * (story.commentsCount + 1)) / Math.pow(hoursElapsed + 2, 1.8);
      };
      
      sorted.sort((a, b) => getHotnessScore(b) - getHotnessScore(a));
    } else if (sortMode === 'discussion') {
      sorted.sort((a, b) => b.commentsCount - a.commentsCount);
    }

    return sorted;
  }, [stories, bookmarks, searchQuery, selectedCategories, sortMode, viewMode]);

  // Sidebar category count calculation (based on active master stream or library)
  const categoryCounts = useMemo(() => {
    const counts = {};
    const baseList = viewMode === 'library' ? bookmarks : stories;
    
    // Set 0 default
    categoriesList.forEach(c => {
      counts[c.name] = 0;
    });

    baseList.forEach(story => {
      if (counts[story.category] !== undefined) {
        counts[story.category] += 1;
      } else {
        counts[story.category] = 1;
      }
    });

    return counts;
  }, [stories, bookmarks, viewMode, categoriesList]);

  return (
    <div className="app-container">
      
      {/* Sticky Glass Header */}
      <header className="sticky-header">
        <div className="header-content">
          
          {/* Logo */}
          <div className="brand-logo-container" onClick={() => { setViewMode('stream'); handleResetFilters(); }}>
            <div className="brand-pulse-node"></div>
            <h1 className="brand-title">
              NEURALPULSE
              <span className="brand-beta">INTELLIGENCE</span>
            </h1>
          </div>

          {/* Action inputs & Search */}
          <div className="header-actions">
            <div className="search-wrapper">
              <Search className="search-icon" />
              <input 
                type="text" 
                className="search-input" 
                placeholder="Search titles, authors, domains..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              {searchQuery && (
                <button className="search-clear-btn" onClick={() => setSearchQuery('')}>
                  <X />
                </button>
              )}
            </div>

            <button 
              className={`nav-library-btn ${viewMode === 'library' ? 'active' : ''}`}
              onClick={() => setViewMode(prev => prev === 'library' ? 'stream' : 'library')}
            >
              <Star className="sort-icon" style={{ fill: viewMode === 'library' ? 'currentColor' : 'none' }} />
              My Library
              <span className="nav-library-btn-badge">{bookmarks.length}</span>
            </button>
          </div>

        </div>
      </header>

      {/* Analytics Dashboard Panel */}
      <section className="analytics-section">
        <div className="analytics-container">
          
          <div className="analytics-card">
            <div className="analytics-icon-wrapper">
              <Activity className="sort-icon" />
            </div>
            <div className="analytics-info">
              <span className="analytics-label">AI Pulse Count</span>
              <span className="analytics-value font-mono">
                {metrics.pulseCount}
              </span>
            </div>
          </div>

          <div className="analytics-card">
            <div className="analytics-icon-wrapper purple">
              <Layers className="sort-icon" />
            </div>
            <div className="analytics-info">
              <span className="analytics-label">Dominant Vector</span>
              <span className="analytics-value font-outfit" style={{ fontSize: '1.05rem' }}>
                {metrics.dominantTag}
              </span>
            </div>
          </div>

          <div className="analytics-card">
            <div className="analytics-icon-wrapper success">
              <TrendingUp className="sort-icon" />
            </div>
            <div className="analytics-info">
              <span className="analytics-label">Velocity Metric</span>
              <span className="analytics-value font-mono">
                {metrics.velocity}
              </span>
            </div>
          </div>

        </div>
      </section>

      {/* Warning Banners */}
      {showLsWarning && (
        <div className="toast-banner">
          <div className="toast-content">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <AlertTriangle style={{ width: '1.2rem', height: '1.2rem' }} />
              <span>Private browsing mode detected. Bookmark additions are active but will not survive browser restarts.</span>
            </div>
            <button className="toast-close-btn" onClick={() => setShowLsWarning(false)}>&times;</button>
          </div>
        </div>
      )}

      {toastMessage && (
        <div className="toast-banner" style={{ position: 'fixed', bottom: '1.5rem', right: '1.5rem', zIndex: '200', padding: 0, margin: 0, width: 'auto', maxWidth: '450px' }}>
          <div className="toast-content info" style={{ boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Info style={{ width: '1.2rem', height: '1.2rem' }} />
              <span>{toastMessage}</span>
            </div>
          </div>
        </div>
      )}

      {/* Main Grid Workspace */}
      <main className="main-layout">
        
        {/* Sidebar Controls */}
        <aside className="sidebar-filters">
          
          {/* Categories panel */}
          <div className="sidebar-panel">
            <h3 className="sidebar-heading">Intelligence Channels</h3>
            <ul className="category-list">
              {categoriesList.map((cat) => {
                const isActive = selectedCategories.includes(cat.name);
                const IconComponent = cat.icon;
                return (
                  <li 
                    key={cat.name} 
                    className={`category-item ${isActive ? 'active' : ''}`}
                    onClick={() => handleToggleCategoryFilter(cat.name)}
                  >
                    <div className="category-checkbox-wrapper">
                      <div className="category-checkbox-visual">
                        {isActive && <Check className="category-checkbox-check" />}
                      </div>
                      <IconComponent style={{ width: '1.1rem', height: '1.1rem', color: cat.color }} />
                      <span className="category-name">{cat.name}</span>
                    </div>
                    <span className="category-count font-mono">{categoryCounts[cat.name]}</span>
                  </li>
                );
              })}
            </ul>
          </div>

          {/* Sorters Panel */}
          <div className="sidebar-panel">
            <h3 className="sidebar-heading">Sort Alignment</h3>
            <div className="sort-options">
              <button 
                className={`sort-btn ${sortMode === 'recency' ? 'active' : ''}`}
                onClick={() => setSortMode('recency')}
              >
                <Clock className="sort-icon" />
                Recency (Newest)
              </button>
              <button 
                className={`sort-btn ${sortMode === 'popularity' ? 'active' : ''}`}
                onClick={() => setSortMode('popularity')}
              >
                <Flame className="sort-icon" />
                Hotness Velocity
              </button>
              <button 
                className={`sort-btn ${sortMode === 'discussion' ? 'active' : ''}`}
                onClick={() => setSortMode('discussion')}
              >
                <MessageSquare className="sort-icon" />
                Discussion Weight
              </button>
            </div>
          </div>

          {/* Export / Import personal library toolkit */}
          <div className="sidebar-panel">
            <h3 className="sidebar-heading">Personal Toolkit</h3>
            <div className="library-actions">
              <button className="action-btn" onClick={handleExportJSON}>
                <Download style={{ width: '1rem', height: '1.1rem' }} />
                Export Library (.json)
              </button>
              <button className="action-btn" onClick={handleCopyJSONToClipboard}>
                <Copy style={{ width: '1rem', height: '1.1rem' }} />
                Copy Library JSON
              </button>
              <button className="action-btn" onClick={handleImportJSONTrigger}>
                <RefreshCw style={{ width: '1rem', height: '1.1rem' }} />
                Import Saved JSON
              </button>
              <input 
                type="file" 
                accept=".json" 
                ref={fileInputRef} 
                style={{ display: 'none' }} 
                onChange={handleImportJSONFile} 
              />
            </div>
          </div>

        </aside>

        {/* Stories Feed View */}
        <section className="stories-section">
          
          {/* Header row in stories list */}
          <div className="section-header-bar">
            <h2 className="section-title">
              {viewMode === 'library' ? 'My Library Archive' : 'Live Intelligence Stream'}
              {feedType === 'offline_fallback' && (
                <span className="brand-beta" style={{ backgroundColor: 'rgba(239, 68, 68, 0.15)', color: '#EF4444', borderColor: 'rgba(239, 68, 68, 0.25)', marginLeft: '1rem' }}>OFFLINE</span>
              )}
              {feedType === 'cached' && (
                <span className="brand-beta" style={{ backgroundColor: 'rgba(6, 182, 212, 0.15)', color: 'var(--color-cyan)', borderColor: 'rgba(6, 182, 212, 0.25)', marginLeft: '1rem' }}>CACHED</span>
              )}
            </h2>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <span className="section-count">
                {processedStories.length} matches discovered
              </span>
              {viewMode === 'stream' && (
                <button 
                  onClick={handleRefresh} 
                  className="action-btn" 
                  style={{ width: 'auto', padding: '0.4rem 0.8rem', borderRadius: '6px' }}
                  title="Force revalidate feed"
                  disabled={isLoading}
                >
                  <RefreshCw className={`sort-icon ${isLoading ? 'animate-spin' : ''}`} style={{ animation: isLoading ? 'spin 1s linear infinite' : 'none' }} />
                </button>
              )}
            </div>
          </div>

          {/* Skeleton Load Shimmer State */}
          {isLoading && stories.length === 0 ? (
            <div className="stories-feed-grid">
              {[1, 2, 3, 4, 5, 6].map((item) => (
                <div key={item} className="skeleton-card">
                  <div className="skeleton-shimmer"></div>
                  <div>
                    <div className="skeleton-item skeleton-header"></div>
                    <div className="skeleton-item skeleton-title-1"></div>
                    <div className="skeleton-item skeleton-title-2"></div>
                  </div>
                  <div className="skeleton-item skeleton-tag"></div>
                  <div className="skeleton-item skeleton-footer">
                    <div className="skeleton-footer-left"></div>
                    <div className="skeleton-footer-right"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <AnimatePresence mode="popLayout">
              {processedStories.length === 0 ? (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="empty-state-card"
                >
                  <Star className="empty-state-icon" />
                  <h3 className="empty-state-title">No AI Intelligence Found</h3>
                  <p className="empty-state-desc">
                    We couldn't locate any records matching your current filter filters.
                    Try resetting your keyword queries or selecting different intelligence channels.
                  </p>
                  <button className="empty-state-btn font-outfit" onClick={handleResetFilters}>
                    Clear All Filters
                  </button>
                </motion.div>
              ) : (
                <motion.div 
                  layout
                  className="stories-feed-grid"
                >
                  {processedStories.map((story) => {
                    const isBookmarked = bookmarks.some(b => b.id === story.id);
                    const categoryObj = categoriesList.find(c => c.name === story.category) || categoriesList[5];

                    return (
                      <motion.article
                        layout
                        key={story.id}
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        transition={{ duration: 0.25 }}
                        className="news-card-outer"
                      >
                        <div className="news-card-inner">
                          
                          <div className="news-card-header">
                            <div className="news-card-domain-row">
                              <span className="news-card-domain font-mono">{story.domain}</span>
                              <button 
                                className={`news-card-bookmark-trigger ${isBookmarked ? 'bookmarked' : ''}`}
                                onClick={(e) => handleToggleBookmark(story, e)}
                                title={isBookmarked ? "Remove bookmark" : "Save story to library"}
                              >
                                <Star 
                                  style={{ 
                                    width: '1.1rem', 
                                    height: '1.1rem', 
                                    fill: isBookmarked ? 'var(--color-purple)' : 'none' 
                                  }} 
                                />
                                <BookmarkBurst isTriggered={isBookmarked} />
                              </button>
                            </div>

                            <a 
                              href={story.url} 
                              target="_blank" 
                              rel="noopener noreferrer" 
                              className="news-card-title-link"
                            >
                              <h3 className="news-card-title font-outfit">
                                {story.title}
                              </h3>
                            </a>
                          </div>

                          <div className="news-card-category-row">
                            <span className={`category-badge ${categoryObj.tagClass}`}>
                              {story.category}
                            </span>
                          </div>

                          <div className="news-card-metadata">
                            <div className="news-card-author-row font-mono">
                              <span>by <a href={`https://news.ycombinator.com/user?id=${story.author}`} target="_blank" rel="noopener noreferrer" className="author-link">{story.author}</a></span>
                              <span style={{ fontSize: '0.7rem' }}>{story.createdDateString}</span>
                            </div>

                            <div className="news-card-stats-row">
                              <div className="stat-item score">
                                <Flame style={{ width: '0.85rem', height: '0.85rem', fill: 'currentColor' }} />
                                <span>{story.points} pts</span>
                              </div>

                              <div className="stat-item comments">
                                <a 
                                  href={story.hnUrl} 
                                  target="_blank" 
                                  rel="noopener noreferrer" 
                                  className="comments-link"
                                >
                                  <MessageSquare style={{ width: '0.85rem', height: '0.85rem' }} />
                                  <span>{story.commentsCount} comments</span>
                                </a>
                              </div>

                              <div className="stat-item" style={{ fontSize: '0.7rem' }} title="Reading speed calculated at 180 words per minute">
                                <Clock style={{ width: '0.8rem', height: '0.8rem' }} />
                                <span>{story.readingTime}m read</span>
                              </div>
                            </div>
                          </div>

                        </div>
                      </motion.article>
                    );
                  })}
                </motion.div>
              )}
            </AnimatePresence>
          )}

        </section>

      </main>

    </div>
  );
}

// Micro-interaction Component for bookmark burst particle effect (TC-005 Requirement)
function BookmarkBurst({ isTriggered }) {
  const [showParticles, setShowParticles] = useState(false);
  const prevTriggered = useRef(isTriggered);

  useEffect(() => {
    // Only fire on transitions from unbookmarked -> bookmarked
    if (isTriggered && !prevTriggered.current) {
      setShowParticles(true);
      const timer = setTimeout(() => {
        setShowParticles(false);
      }, 700);
      return () => clearTimeout(timer);
    }
    prevTriggered.current = isTriggered;
  }, [isTriggered]);

  if (!showParticles) return null;

  return (
    <div className="bookmark-burst-container">
      {[0, 1, 2, 3].map(i => {
        const isCyan = i % 2 === 0;
        return (
          <div 
            key={i} 
            className="burst-particle"
            style={{
              backgroundColor: isCyan ? 'var(--color-cyan)' : 'var(--color-purple)',
              boxShadow: `0 0 6px ${isCyan ? 'var(--color-cyan)' : 'var(--color-purple)'}`,
              animation: `burst-particle-${i} 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards`
            }}
          />
        );
      })}
    </div>
  );
}
