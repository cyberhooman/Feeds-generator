"""
Slide Validator - Quality Gate for Professional Output

Validates slides before rendering to ensure:
1. Text fits within slide bounds (no overflow)
2. Professional tone is maintained
3. Visual quality meets standards
4. Layout balance is good
5. Typography is optimized

Acts as a quality gate to prevent unprofessional output.
"""

import logging
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"  # Must fix - prevents rendering
    WARNING = "warning"  # Should fix - renders but not optimal
    INFO = "info"  # FYI - no action needed


@dataclass
class ValidationIssue:
    """A validation issue found in a slide."""
    slide_number: int
    level: ValidationLevel
    category: str  # "text_overflow", "professional_tone", "visual_quality", etc.
    message: str
    recommendation: str
    severity_score: float  # 0-10, higher = more severe


@dataclass
class ValidationResult:
    """Result of slide validation."""
    is_valid: bool
    total_issues: int
    errors: List[ValidationIssue]
    warnings: List[ValidationIssue]
    info: List[ValidationIssue]
    professional_score: float  # 0-100
    overall_quality_score: float  # 0-100


class SlideValidator:
    """
    Validates carousel slides for professional quality before rendering.

    Philosophy:
    - TEXT MUST FIT: No overflow allowed
    - PROFESSIONAL TONE: No AI-detection red flags
    - VISUAL BALANCE: Good text/image ratio
    - TYPOGRAPHY: Readable and well-spaced
    """

    def __init__(self):
        """Initialize the slide validator."""
        # Professional tone red flags (AI-detection markers)
        self.ai_tone_red_flags = [
            r'\bin today[\'s]* world\b',
            r'\blet[\'s]* dive (in|into)\b',
            r'\bwithout further ado\b',
            r'\bas (we|you|one) (can see|know|might think)\b',
            r'\bit[\'s]* important to (note|remember|mention)\b',
            r'\bin conclusion\b',
            r'\bfurthermore\b',
            r'\bmoreover\b',
            r'\bnevertheless\b',
            r'\bin fact\b',
            r'\btruly revolutionary\b',
            r'\bunlock your potential\b',
        ]

        # Professional tone positive markers
        self.professional_markers = [
            r'\b\d+%\b',  # statistics
            r'\$\d+[kK]?\b',  # currency
            r'\bstudies? (show|found|indicate)\b',
            r'\bdata\b',
            r'\bproof\b',
            r'\brecent(ly)?\b',
            r'\bconcrete\b',
        ]

    def validate_slide(
        self,
        slide_number: int,
        text: str,
        total_slides: int,
        has_visual: bool = False
    ) -> List[ValidationIssue]:
        """
        Validate a single slide.

        Args:
            slide_number: Slide number (1-indexed)
            text: Clean slide text
            total_slides: Total slides in carousel
            has_visual: Whether slide has a visual

        Returns:
            List of ValidationIssues found
        """
        issues = []

        # Check 1: Text overflow
        issues.extend(self._check_text_overflow(slide_number, text))

        # Check 2: Professional tone
        issues.extend(self._check_professional_tone(slide_number, text))

        # Check 3: Text length appropriateness
        issues.extend(self._check_text_length(slide_number, text, total_slides))

        # Check 4: Visual balance
        if has_visual:
            issues.extend(self._check_visual_balance(slide_number, text, total_slides))

        # Check 5: Typography quality
        issues.extend(self._check_typography(slide_number, text))

        return issues

    def _check_text_overflow(self, slide_number: int, text: str) -> List[ValidationIssue]:
        """Check if text would overflow the slide bounds."""
        issues = []

        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        text_length = len(clean_text)

        # Define safe limits
        hook_max = 150  # Hook slide (slide 1)
        body_max = 350  # Body slides
        cta_max = 180   # CTA slide

        if slide_number == 1:
            max_length = hook_max
            slide_type = "Hook"
        elif slide_number % 2 == 0:  # Last slide is typically even in small carousels
            max_length = cta_max
            slide_type = "CTA"
        else:
            max_length = body_max
            slide_type = "Body"

        if text_length > max_length * 1.5:  # 50% over limit = ERROR
            issues.append(ValidationIssue(
                slide_number=slide_number,
                level=ValidationLevel.ERROR,
                category="text_overflow",
                message=f"Text is too long ({text_length} chars vs {max_length} limit)",
                recommendation=f"Truncate to under {max_length} characters or split across slides",
                severity_score=9.0
            ))
        elif text_length > max_length:  # Over limit = WARNING
            issues.append(ValidationIssue(
                slide_number=slide_number,
                level=ValidationLevel.WARNING,
                category="text_overflow",
                message=f"Text is slightly over recommended limit ({text_length} vs {max_length})",
                recommendation=f"Trim a few words for better readability",
                severity_score=5.0
            ))

        return issues

    def _check_professional_tone(self, slide_number: int, text: str) -> List[ValidationIssue]:
        """Check if text maintains professional tone."""
        issues = []
        text_lower = text.lower()

        # Check for AI red flags
        ai_flags_found = []
        for pattern in self.ai_tone_red_flags:
            if re.search(pattern, text_lower, re.IGNORECASE):
                ai_flags_found.append(pattern)

        if ai_flags_found:
            issues.append(ValidationIssue(
                slide_number=slide_number,
                level=ValidationLevel.WARNING,
                category="professional_tone",
                message=f"Found {len(ai_flags_found)} AI-detection red flags",
                recommendation="Replace generic phrases with specific, authentic language",
                severity_score=6.0
            ))

        # Check for zero professional markers (concerning for content credibility)
        professional_count = sum(1 for pattern in self.professional_markers if re.search(pattern, text_lower))

        # For body slides, having data/proof is good
        if 1 < slide_number < 5 and professional_count == 0:
            issues.append(ValidationIssue(
                slide_number=slide_number,
                level=ValidationLevel.INFO,
                category="professional_tone",
                message="No concrete data or statistics included",
                recommendation="Consider adding numbers, percentages, or proof",
                severity_score=2.0
            ))

        return issues

    def _check_text_length(self, slide_number: int, text: str, total_slides: int) -> List[ValidationIssue]:
        """Check if text length is appropriate for slide type."""
        issues = []

        clean_text = re.sub(r'<[^>]+>', '', text)
        text_length = len(clean_text)

        # Hook slides should be short and punchy
        if slide_number == 1:
            if text_length < 30:
                issues.append(ValidationIssue(
                    slide_number=slide_number,
                    level=ValidationLevel.INFO,
                    category="text_length",
                    message="Hook slide is very short",
                    recommendation="Hook can be longer, but super short is fine if punchy",
                    severity_score=1.0
                ))
            elif text_length > 150:
                issues.append(ValidationIssue(
                    slide_number=slide_number,
                    level=ValidationLevel.WARNING,
                    category="text_length",
                    message="Hook slide is too long - may not grab attention",
                    recommendation="Shorten to under 100 chars for maximum impact",
                    severity_score=4.0
                ))

        # CTA slides should be short and action-oriented
        if slide_number == total_slides:
            if text_length > 150:
                issues.append(ValidationIssue(
                    slide_number=slide_number,
                    level=ValidationLevel.WARNING,
                    category="text_length",
                    message="CTA slide is too long - dilutes call to action",
                    recommendation="Keep CTA under 100 chars, action-oriented",
                    severity_score=5.0
                ))

        return issues

    def _check_visual_balance(self, slide_number: int, text: str, total_slides: int) -> List[ValidationIssue]:
        """Check if text/visual ratio is balanced."""
        issues = []

        clean_text = re.sub(r'<[^>]+>', '', text)
        text_length = len(clean_text)

        # For body slides with visuals, text should be 50-200 chars
        if 1 < slide_number < total_slides:
            if text_length < 20:
                issues.append(ValidationIssue(
                    slide_number=slide_number,
                    level=ValidationLevel.WARNING,
                    category="visual_balance",
                    message="Text is too short for body slide with visual",
                    recommendation="Add context or explanation to make visual meaningful",
                    severity_score=3.0
                ))

        return issues

    def _check_typography(self, slide_number: int, text: str) -> List[ValidationIssue]:
        """Check typography quality."""
        issues = []

        clean_text = re.sub(r'<[^>]+>', '', text)

        # Check for excessive punctuation
        exclamation_count = clean_text.count('!')
        question_count = clean_text.count('?')

        if exclamation_count > 3:
            issues.append(ValidationIssue(
                slide_number=slide_number,
                level=ValidationLevel.INFO,
                category="typography",
                message=f"Excessive exclamation marks ({exclamation_count})",
                recommendation="Reduce to 1-2 for professional appearance",
                severity_score=2.0
            ))

        # Check for all caps (can appear aggressive)
        all_caps_words = len([w for w in clean_text.split() if w.isupper() and len(w) > 1])
        if all_caps_words > 2:
            issues.append(ValidationIssue(
                slide_number=slide_number,
                level=ValidationLevel.WARNING,
                category="typography",
                message=f"Multiple ALL CAPS words ({all_caps_words})",
                recommendation="Use normal capitalization for professional tone",
                severity_score=3.0
            ))

        return issues

    def validate_carousel(
        self,
        slides: List[str],
        has_visuals: Optional[List[bool]] = None
    ) -> ValidationResult:
        """
        Validate entire carousel.

        Args:
            slides: List of slide texts
            has_visuals: Optional list of bools indicating if each slide has visual

        Returns:
            ValidationResult with all issues and scores
        """
        if has_visuals is None:
            has_visuals = [True] * len(slides)

        all_issues = []
        total_slides = len(slides)

        logger.info(f"Validating carousel with {total_slides} slides...")

        for i, slide_text in enumerate(slides, 1):
            issues = self.validate_slide(
                slide_number=i,
                text=slide_text,
                total_slides=total_slides,
                has_visual=has_visuals[i - 1] if i <= len(has_visuals) else True
            )
            all_issues.extend(issues)

        # Categorize issues
        errors = [issue for issue in all_issues if issue.level == ValidationLevel.ERROR]
        warnings = [issue for issue in all_issues if issue.level == ValidationLevel.WARNING]
        infos = [issue for issue in all_issues if issue.level == ValidationLevel.INFO]

        # Calculate scores
        total_severity = sum(issue.severity_score for issue in all_issues)
        professional_score = max(0, 100 - (sum(issue.severity_score for issue in warnings + infos) * 2))
        overall_quality_score = max(0, 100 - (sum(issue.severity_score for issue in all_issues) * 1.5))

        is_valid = len(errors) == 0

        logger.info(f"✓ Carousel validation: {len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")
        logger.info(f"  Professional score: {professional_score:.0f}/100")
        logger.info(f"  Quality score: {overall_quality_score:.0f}/100")

        return ValidationResult(
            is_valid=is_valid,
            total_issues=len(all_issues),
            errors=errors,
            warnings=warnings,
            info=infos,
            professional_score=professional_score,
            overall_quality_score=overall_quality_score
        )


# Convenience function
def validate_carousel_quality(
    slides: List[str],
    strict_mode: bool = False
) -> Dict[str, any]:
    """
    Quick validation function for carousel slides.

    Args:
        slides: List of slide texts
        strict_mode: If True, warnings are treated as errors

    Returns:
        Dict with validation results
    """
    validator = SlideValidator()
    result = validator.validate_carousel(slides)

    return {
        'is_valid': result.is_valid and (not strict_mode or len(result.warnings) == 0),
        'professional_score': result.professional_score,
        'quality_score': result.overall_quality_score,
        'total_issues': result.total_issues,
        'errors': len(result.errors),
        'warnings': len(result.warnings),
        'issues': [
            {
                'slide': issue.slide_number,
                'level': issue.level.value,
                'category': issue.category,
                'message': issue.message,
                'recommendation': issue.recommendation
            }
            for issue in result.errors + result.warnings
        ]
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("Testing SlideValidator...")
    print("=" * 80)

    test_slides = [
        "Tapi creator economy bukan cuma soal influencer.",
        "Ini soal transformasi fundamental dan perubahan paradigma dalam digital era.",
        "Ada 50 juta+ creator di Indonesia dengan pertumbuhan 300% per tahun.",
        "Followers gua minimal 100k, eh dibayar cuma 10k per post?",
        "Follow untuk tips creator lainnya dan jangan lewatkan konten menarik berikutnya!",
    ]

    validator = SlideValidator()
    result = validator.validate_carousel(test_slides)

    print("\nVALIDATION RESULTS:")
    print(f"Valid: {result.is_valid}")
    print(f"Professional Score: {result.professional_score:.0f}/100")
    print(f"Quality Score: {result.overall_quality_score:.0f}/100")
    print(f"Total Issues: {result.total_issues}")

    if result.errors:
        print("\n❌ ERRORS:")
        for err in result.errors:
            print(f"  Slide {err.slide_number}: {err.message}")

    if result.warnings:
        print("\n⚠️  WARNINGS:")
        for warn in result.warnings:
            print(f"  Slide {warn.slide_number}: {warn.message}")

    print("\n" + "=" * 80)
    print("Done!")
