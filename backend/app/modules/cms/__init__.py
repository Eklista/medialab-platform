"""
CMS Module - Universidad Galileo MediaLab Platform

This module handles all content management functionality for the MediaLab platform.
It provides a comprehensive system for organizing and publishing multimedia content
with smart filtering and categorization.

RESPONSIBILITIES:
- Content creation and management (videos, galleries)
- Category-based organization with academic unit filtering
- Content publishing workflow and visibility control
- SEO optimization with slugs and metadata
- Simple analytics and view tracking

CORE COMPONENTS:
- models/: Database models for content entities
- schemas/: Pydantic models for API validation
- services/: Business logic for content operations
- repositories/: Data access layer for content data
- router.py: API endpoints for content management

CONTENT TYPES:
- Video: YouTube embeds with metadata and categorization
- Gallery: Photo collections with bulk upload support
- Category: Smart filtering by academic unit and content type

FILTERING ARCHITECTURE:
Academic Unit (FISICC) → Category (Graduación) → Content (Videos + Galleries)

This module enables MediaLab to publish and organize content efficiently
while providing intelligent filtering for end users based on their interests
and academic unit affiliations.
"""