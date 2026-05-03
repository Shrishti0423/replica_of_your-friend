#!/usr/bin/env python3
"""
Personality Analyzer - Analyzes chat data to extract personality traits
Generates dynamic personality profiles for creating chat replicas
"""

import json
from typing import List, Dict, Any
from collections import Counter
import re

class PersonalityAnalyzer:
    def __init__(self):
        self.messages = []
        self.personality_profile = {}
    
    def analyze_chat_data(self, messages: List[Dict[str, Any]], person_name: str = "Person") -> Dict[str, Any]:
        """
        Analyze chat messages and extract personality traits
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            person_name: Name of the person to analyze
            
        Returns:
            Dictionary with personality profile
        """
        self.messages = [m for m in messages if m.get('role') == 'user']
        
        if not self.messages:
            return self._create_default_profile(person_name)
        
        profile = {
            'name': person_name,
            'message_count': len(self.messages),
            'communication_style': self._analyze_communication_style(),
            'common_topics': self._extract_common_topics(),
            'frequent_phrases': self._extract_frequent_phrases(),
            'emotional_traits': self._analyze_emotional_traits(),
            'language_patterns': self._analyze_language_patterns(),
            'typical_requests': self._extract_typical_requests(),
            'interests': self._extract_interests(),
            'tone': self._analyze_tone(),
            'vocabulary_level': self._analyze_vocabulary_level()
        }
        
        self.personality_profile = profile
        return profile
    
    def _analyze_communication_style(self) -> str:
        """Analyze if the person is casual, formal, direct, etc."""
        content = ' '.join([m.get('content', '') for m in self.messages])
        
        casual_markers = ['lol', 'haha', 'omg', 'yeah', 'hey', 'hi', 'yo', 'dude', 'bro', 'cool', 'awesome']
        formal_markers = ['please', 'kindly', 'regarding', 'however', 'therefore', 'dear']
        direct_markers = ['need', 'want', 'must', 'require', 'bring', 'get', 'do this']
        
        casual_count = sum(1 for marker in casual_markers if marker in content.lower())
        formal_count = sum(1 for marker in formal_markers if marker in content.lower())
        direct_count = sum(1 for marker in direct_markers if marker in content.lower())
        
        style = []
        if casual_count > formal_count:
            style.append('casual')
        if formal_count > casual_count:
            style.append('formal')
        if direct_count > len(self.messages) / 4:
            style.append('direct')
        
        avg_msg_length = sum(len(m.get('content', '').split()) for m in self.messages) / len(self.messages)
        if avg_msg_length < 10:
            style.append('short and concise')
        elif avg_msg_length > 50:
            style.append('detailed and verbose')
        
        return ', '.join(style) if style else 'conversational'
    
    def _extract_common_topics(self) -> List[str]:
        """Extract common topics from messages"""
        content = ' '.join([m.get('content', '') for m in self.messages]).lower()
        
        topic_keywords = {
            'food': ['food', 'eat', 'eating', 'lunch', 'dinner', 'breakfast', 'snack', 'recipe', 'cook', 'cooking', 'momos', 'pizza', 'burger'],
            'work': ['work', 'job', 'office', 'company', 'project', 'deadline', 'meeting', 'boss', 'colleague'],
            'family': ['mom', 'dad', 'sister', 'brother', 'family', 'cousin', 'aunt', 'uncle', 'parent'],
            'school': ['school', 'college', 'university', 'class', 'exam', 'study', 'homework', 'assignment', 'test'],
            'travel': ['travel', 'trip', 'visit', 'airport', 'flight', 'vacation', 'tour', 'place'],
            'health': ['health', 'doctor', 'medicine', 'sick', 'ill', 'exercise', 'gym', 'diet', 'fitness'],
            'technology': ['code', 'programming', 'computer', 'software', 'app', 'tech', 'python', 'javascript'],
            'entertainment': ['movie', 'watch', 'show', 'music', 'game', 'play', 'fun', 'enjoy'],
            'shopping': ['buy', 'shop', 'store', 'mall', 'price', 'cost', 'amazon', 'shopping', 'purchase'],
            'relationship': ['love', 'like', 'friend', 'boyfriend', 'girlfriend', 'date', 'relationship']
        }
        
        topics = []
        for topic, keywords in topic_keywords.items():
            count = sum(content.count(keyword) for keyword in keywords)
            if count > 0:
                topics.append((topic, count))
        
        # Sort by frequency and return top 5
        topics.sort(key=lambda x: x[1], reverse=True)
        return [topic[0] for topic in topics[:5]]
    
    def _extract_frequent_phrases(self) -> List[str]:
        """Extract frequently used phrases"""
        content = ' '.join([m.get('content', '') for m in self.messages])
        
        # Extract 2-3 word phrases
        words = content.lower().split()
        phrases = []
        
        for i in range(len(words) - 2):
            phrase = ' '.join(words[i:i+3])
            if len(phrase) > 5:  # Avoid very short phrases
                phrases.append(phrase)
        
        phrase_freq = Counter(phrases)
        common_phrases = [phrase for phrase, count in phrase_freq.most_common(10) if count >= 2]
        
        return common_phrases[:5] if common_phrases else ['conversation', 'hello', 'thanks']
    
    def _analyze_emotional_traits(self) -> List[str]:
        """Analyze emotional characteristics"""
        content = ' '.join([m.get('content', '') for m in self.messages]).lower()
        
        traits = []
        
        if any(word in content for word in ['please', 'thanks', 'thank you', 'appreciate', 'grateful']):
            traits.append('polite')
        if any(word in content for word in ['love', 'amazing', 'awesome', 'great', 'excellent', 'wonderful']):
            traits.append('positive')
        if any(word in content for word in ['sad', 'angry', 'upset', 'frustrated', 'annoyed']):
            traits.append('expressive')
        if any(word in content for word in ['sorry', 'apologize', 'mistake', 'wrong']):
            traits.append('reflective')
        if any(word in content for word in ['help', 'support', 'care', 'concern']):
            traits.append('caring')
        if any(word in content for word in ['must', 'need', 'want', 'demand', 'require']):
            traits.append('assertive')
        if '!' in content or '!!!' in content:
            traits.append('enthusiastic')
        if '?' in content:
            exclamation_ratio = content.count('?') / len(self.messages)
            if exclamation_ratio > 0.3:
                traits.append('curious')
        
        return traits if traits else ['friendly', 'conversational']
    
    def _analyze_language_patterns(self) -> List[str]:
        """Detect language patterns like Hinglish, emojis, etc."""
        content = ' '.join([m.get('content', '') for m in self.messages])
        
        patterns = []
        
        # Detect emojis
        emoji_pattern = r'[^\w\s]'
        if len(re.findall(emoji_pattern, content)) > len(self.messages):
            patterns.append('uses emojis frequently')
        
        # Detect Hindi words (common ones)
        hindi_words = ['kya', 'haal', 'kaku', 'mere', 'lekar', 'ana', 'kb', 'ayegi', 'plz', 'yr', 'mujhe', 'na', 'hn']
        if any(word in content.lower() for word in hindi_words):
            patterns.append('Hinglish (Hindi + English)')
        
        # Detect capitalization patterns
        caps_words = len([w for w in content.split() if w.isupper() and len(w) > 1])
        if caps_words > len(self.messages) / 5:
            patterns.append('uses caps for emphasis')
        
        # Detect ellipsis
        if '...' in content:
            patterns.append('uses ellipsis')
        
        # Detect contractions
        if any(contraction in content.lower() for contraction in ["don't", "can't", "won't", "it's", "i'm"]):
            patterns.append('uses contractions')
        
        return patterns if patterns else ['standard English']
    
    def _extract_typical_requests(self) -> List[str]:
        """Extract what this person typically asks for"""
        content = ' '.join([m.get('content', '') for m in self.messages]).lower()
        
        requests = []
        
        request_patterns = {
            'bring food': ['bring me', 'get me food', 'bring food', 'fetch me'],
            'shopping': ['buy this', 'get this', 'purchase', 'shopping', 'from store'],
            'rides': ['pick me up', 'come pick', 'give me ride', 'drive me'],
            'information': ['tell me', 'what is', 'how to', 'explain', 'information about'],
            'help': ['help me', 'can you help', 'assist me', 'support'],
            'meetings': ['when are you coming', 'when will you', 'lets meet', 'see you']
        }
        
        for request_type, patterns in request_patterns.items():
            if any(pattern in content for pattern in patterns):
                requests.append(request_type)
        
        return requests if requests else ['general conversation']
    
    def _extract_interests(self) -> List[str]:
        """Extract interests and hobbies"""
        content = ' '.join([m.get('content', '') for m in self.messages]).lower()
        
        interests = {
            'cooking': ['cook', 'recipe', 'food', 'kitchen', 'chef', 'pasta', 'pizza'],
            'gaming': ['game', 'play', 'console', 'steam', 'online', 'fps'],
            'music': ['music', 'song', 'listen', 'artist', 'concert', 'spotify'],
            'sports': ['sport', 'play', 'team', 'game', 'match', 'score', 'basketball'],
            'reading': ['read', 'book', 'novel', 'story', 'author', 'page'],
            'art': ['draw', 'paint', 'art', 'creative', 'design', 'color'],
            'travel': ['travel', 'trip', 'visit', 'explore', 'adventure', 'place'],
            'tech': ['code', 'program', 'computer', 'tech', 'software', 'app']
        }
        
        found_interests = []
        for interest, keywords in interests.items():
            if any(keyword in content for keyword in keywords):
                found_interests.append(interest)
        
        return found_interests[:5] if found_interests else []
    
    def _analyze_tone(self) -> str:
        """Analyze overall tone"""
        content = ' '.join([m.get('content', '') for m in self.messages]).lower()
        
        positive_words = ['great', 'love', 'awesome', 'amazing', 'wonderful', 'excellent', 'happy', 'good']
        negative_words = ['hate', 'bad', 'terrible', 'awful', 'sad', 'angry', 'frustrated']
        
        positive_count = sum(content.count(word) for word in positive_words)
        negative_count = sum(content.count(word) for word in negative_words)
        
        if positive_count > negative_count:
            return 'positive and upbeat'
        elif negative_count > positive_count:
            return 'critical and expressive'
        else:
            return 'neutral and balanced'
    
    def _analyze_vocabulary_level(self) -> str:
        """Analyze vocabulary complexity"""
        content = ' '.join([m.get('content', '') for m in self.messages])
        words = content.split()
        
        if not words:
            return 'conversational'
        
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        if avg_word_length < 4:
            return 'simple and casual'
        elif avg_word_length < 5.5:
            return 'conversational'
        else:
            return 'sophisticated and detailed'
    
    def _create_default_profile(self, person_name: str) -> Dict[str, Any]:
        """Create a default profile when no messages found"""
        return {
            'name': person_name,
            'message_count': 0,
            'communication_style': 'conversational',
            'common_topics': ['general'],
            'frequent_phrases': ['hello', 'thanks', 'okay'],
            'emotional_traits': ['friendly'],
            'language_patterns': ['standard English'],
            'typical_requests': ['information'],
            'interests': [],
            'tone': 'neutral',
            'vocabulary_level': 'conversational'
        }
    
    def generate_system_prompt(self, profile: Dict[str, Any], custom_name: str = None) -> str:
        """
        Generate a system prompt for the chatbot based on personality profile
        
        Args:
            profile: Personality profile dictionary
            custom_name: Optional custom name for the person
            
        Returns:
            System prompt string for OpenAI API
        """
        name = custom_name or profile.get('name', 'Person')
        
        prompt = f"""You are {name}, a person with the following characteristics:

PERSONALITY TRAITS:
- Communication Style: {profile.get('communication_style', 'conversational')}
- Tone: {profile.get('tone', 'neutral')}
- Emotional Traits: {', '.join(profile.get('emotional_traits', ['friendly']))}
- Vocabulary Level: {profile.get('vocabulary_level', 'conversational')}

LANGUAGE PATTERNS:
- {chr(10).join(['- ' + pattern for pattern in profile.get('language_patterns', ['standard English'])])}

INTERESTS & TOPICS:
- Common Topics: {', '.join(profile.get('common_topics', ['general conversation']))}
- Interests: {', '.join(profile.get('interests', [])) if profile.get('interests') else 'various'}

TYPICAL BEHAVIOR:
- Usually asks about: {', '.join(profile.get('typical_requests', ['information']))}
- Frequent phrases: {', '.join(profile.get('frequent_phrases', ['hello', 'thanks']))}

INSTRUCTIONS:
- Respond naturally as {name} would
- Use your characteristic communication style
- Maintain your personality traits and tone
- Match your typical language patterns
- Keep responses authentic and consistent with your profile
- Be yourself - don't pretend to be someone else

IMPORTANT: Stay in character and respond like {name} would in real conversation."""
        
        return prompt
    
    def get_profile_summary(self) -> str:
        """Get a human-readable summary of the personality profile"""
        profile = self.personality_profile
        
        summary = f"""
PERSONALITY PROFILE ANALYSIS
{'='*50}

Name: {profile.get('name', 'Unknown')}
Messages Analyzed: {profile.get('message_count', 0)}

Communication Style: {profile.get('communication_style', 'N/A')}
Tone: {profile.get('tone', 'N/A')}
Vocabulary: {profile.get('vocabulary_level', 'N/A')}

Emotional Traits: {', '.join(profile.get('emotional_traits', []))}
Language Patterns: {', '.join(profile.get('language_patterns', []))}

Common Topics: {', '.join(profile.get('common_topics', []))}
Interests: {', '.join(profile.get('interests', [])) if profile.get('interests') else 'Not identified'}

Typical Requests: {', '.join(profile.get('typical_requests', []))}
Frequent Phrases: {', '.join(profile.get('frequent_phrases', []))}

{'='*50}
"""
        return summary
