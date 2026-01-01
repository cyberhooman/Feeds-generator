"""
Main CLI Interface for Meme Content Studio

Command-line interface for creating human-sounding Instagram carousels.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from pathlib import Path
from typing import Optional
import json

from .rewriter import ContentRewriter
from .humanizer import Humanizer
from .meme_matcher import MemeMatcher
from .caption_generator import CaptionGenerator
from .slide_generator import SlideGenerator
from .config import Config

app = typer.Typer(help="Meme Content Studio - Create 100% human-sounding Instagram carousels")
console = Console()


@app.command()
def create(
    content: str = typer.Option(..., "--content", "-c", help="Your rough idea for the carousel"),
    tone: str = typer.Option("santai_gaul", "--tone", "-t", help="Tone to use (e.g., santai_gaul, profesional, casual_friendly)"),
    language: str = typer.Option("bahasa", "--lang", "-l", help="Language: bahasa, english, or mixed"),
    angle: str = typer.Option("story_personal", "--angle", "-a", help="Content angle (e.g., story_personal, hot_take, tips_listicle)"),
    versions: int = typer.Option(1, "--versions", "-v", help="Number of versions to generate"),
    meme: Optional[str] = typer.Option(None, "--meme", "-m", help="Specific meme filename to use (overrides auto-matching)"),
    skip_humanizer: bool = typer.Option(False, "--skip-humanizer", help="Skip humanization check"),
    output_name: str = typer.Option("carousel", "--output", "-o", help="Output project name")
):
    """
    Create a new Instagram carousel from your rough idea.
    """
    console.print("\n[bold cyan]🎨 Meme Content Studio[/bold cyan]")
    console.print("[dim]Creating content that looks 100% human-made...[/dim]\n")

    try:
        # Step 1: Rewrite content
        with console.status("[bold green]Rewriting content with professional copywriter brain..."):
            rewriter = ContentRewriter()
            content_versions = rewriter.rewrite_content(
                rough_idea=content,
                tone=tone,
                language=language,
                angle=angle,
                versions=versions
            )

        console.print(f"[green]✓[/green] Generated {len(content_versions)} version(s)\n")

        # Display versions
        for idx, version in enumerate(content_versions):
            console.print(f"[bold]Version {idx + 1}:[/bold]")
            console.print(f"  Slides: {len(version['slides'])}")
            console.print(f"  Hook alternatives: {len(version.get('hook_alternatives', []))}\n")

        # Use first version for now (can be extended for user selection)
        selected_version = content_versions[0]
        slides = selected_version['slides']

        # Display slides
        for i, slide in enumerate(slides):
            panel = Panel(
                slide,
                title=f"[bold]Slide {i+1}[/bold] {'(Hook)' if i == 0 else ''}",
                border_style="cyan"
            )
            console.print(panel)

        # Step 2: Humanization check (unless skipped)
        if not skip_humanizer:
            console.print("\n[bold yellow]Running humanization check...[/bold yellow]")
            humanizer = Humanizer()

            needs_improvement = []
            for i, slide in enumerate(slides):
                score = humanizer.calculate_human_score(slide)
                if not score["passes_threshold"]:
                    needs_improvement.append((i, slide, score))

            if needs_improvement:
                console.print(f"[yellow]⚠[/yellow]  {len(needs_improvement)} slide(s) need humanization\n")

                for slide_idx, slide_text, score in needs_improvement:
                    console.print(f"[dim]Slide {slide_idx + 1}: Score {score['score']}/100[/dim]")

                # Auto-humanize
                with console.status("[bold green]Humanizing content..."):
                    humanized_results = humanizer.batch_humanize_slides(slides)

                # Update slides with humanized versions
                slides = [result["humanized"] for result in humanized_results]

                console.print("[green]✓[/green] Humanization complete\n")
            else:
                console.print("[green]✓[/green] All slides sound human!\n")

        # Step 3: Meme matching
        console.print("[bold yellow]Analyzing emotional beats and matching memes...[/bold yellow]")
        matcher = MemeMatcher()

        if not matcher.metadata:
            console.print("[yellow]⚠[/yellow]  No meme library found. Skipping meme matching.\n")
            console.print("[dim]  Add memes to meme_library/images/ and metadata to meme_library/metadata.json[/dim]\n")
            meme_matches = []
        else:
            with console.status("[bold green]Matching memes..."):
                emotions = matcher.analyze_content_emotions(slides)
                meme_matches = matcher.match_memes(slides, emotions)

            console.print("[green]✓[/green] Meme matching complete\n")

            # Display meme recommendations
            for match in meme_matches:
                slide_num = match.get("slide_num", 0)
                recs = match.get("recommendations", [])

                if recs:
                    console.print(f"[bold]Slide {slide_num} meme suggestions:[/bold]")
                    for rec in recs[:2]:  # Show top 2
                        console.print(f"  • {rec['filename']} (confidence: {rec['confidence']}/10)")
                        console.print(f"    [dim]{rec.get('reason', 'N/A')}[/dim]")
                    console.print()

        # Step 4: Generate slides
        console.print("[bold yellow]Generating carousel slides...[/bold yellow]")

        generator = SlideGenerator()

        # Prepare slides data
        slides_data = []
        for i, slide_text in enumerate(slides):
            slide_info = {
                "text": slide_text,
                "is_hook": i == 0
            }

            # Add meme if matched
            if i < len(meme_matches):
                match = meme_matches[i]
                if match.get("recommendations"):
                    best_meme = match["recommendations"][0]
                    meme_path = matcher.get_meme_path(best_meme["filename"])
                    if meme_path:
                        slide_info["meme_path"] = str(meme_path)

            slides_data.append(slide_info)

        # Generate
        with console.status("[bold green]Creating slide images..."):
            generated_paths = generator.generate_carousel(
                slides_data=slides_data,
                project_name=output_name
            )

        console.print(f"[green]✓[/green] Generated {len(generated_paths)} slides\n")

        # Step 5: Generate caption
        console.print("[bold yellow]Generating Instagram caption...[/bold yellow]")

        caption_gen = CaptionGenerator()
        with console.status("[bold green]Writing caption..."):
            captions = caption_gen.generate_caption(
                slides=slides,
                tone=tone,
                language=language,
                versions=2
            )

        console.print(f"[green]✓[/green] Generated {len(captions)} caption variation(s)\n")

        # Display captions
        for idx, cap_data in enumerate(captions):
            strategy = cap_data.get("strategy", f"Version {idx+1}")
            caption = cap_data.get("caption", "")
            hashtags = " ".join(cap_data.get("hashtags", []))

            panel_content = f"{caption}\n\n{hashtags}" if hashtags else caption

            panel = Panel(
                panel_content,
                title=f"[bold]Caption: {strategy}[/bold]",
                border_style="magenta"
            )
            console.print(panel)

        # Save project summary
        project_dir = Config.OUTPUT_DIR / output_name
        summary = {
            "content_input": content,
            "tone": tone,
            "language": language,
            "angle": angle,
            "slides": slides,
            "captions": captions,
            "generated_images": [str(p) for p in generated_paths]
        }

        summary_path = project_dir / "project_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        # Final summary
        console.print("\n[bold green]✅ Carousel created successfully![/bold green]\n")
        console.print(f"[cyan]📁 Output:[/cyan] {project_dir}")
        console.print(f"[cyan]🖼️  Slides:[/cyan] {len(generated_paths)} images generated")
        console.print(f"[cyan]📝 Summary:[/cyan] {summary_path}\n")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}\n")
        raise typer.Exit(1)


@app.command()
def check(
    text: str = typer.Argument(..., help="Text to check for human score")
):
    """
    Check human score of text.
    """
    humanizer = Humanizer()
    report = humanizer.quick_check(text)

    console.print("\n[bold cyan]Human Score Analysis[/bold cyan]")
    console.print(report)


@app.command()
def list_tones(
    language: Optional[str] = typer.Option(None, "--lang", "-l", help="Filter by language: bahasa, english, or mixed")
):
    """
    List available tones.
    """
    console.print("\n[bold cyan]Available Tones[/bold cyan]\n")

    lang_dirs = {
        "bahasa": Config.TONES_DIR / "bahasa",
        "english": Config.TONES_DIR / "english",
        "mixed": Config.TONES_DIR / "mixed"
    }

    for lang, dir_path in lang_dirs.items():
        if language and language != lang:
            continue

        if dir_path.exists():
            console.print(f"[bold]{lang.upper()}:[/bold]")
            tones = [f.stem for f in dir_path.glob("*.txt")]
            for tone in tones:
                console.print(f"  • {tone}")
            console.print()


@app.command()
def list_angles():
    """
    List available content angles.
    """
    console.print("\n[bold cyan]Available Content Angles[/bold cyan]\n")

    if Config.ANGLES_DIR.exists():
        angles = [f.stem for f in Config.ANGLES_DIR.glob("*.txt")]
        for angle in angles:
            console.print(f"  • {angle}")
        console.print()


@app.command()
def list_memes():
    """
    List available memes in library.
    """
    matcher = MemeMatcher()
    memes = matcher.list_available_memes()

    if not memes:
        console.print("\n[yellow]No memes found in library.[/yellow]")
        console.print(f"[dim]Add memes to: {Config.MEME_IMAGES_DIR}[/dim]\n")
        return

    console.print(f"\n[bold cyan]Meme Library ({len(memes)} memes)[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Filename", style="cyan")
    table.add_column("Exists", justify="center")
    table.add_column("Emotions")
    table.add_column("Energy")

    for meme in memes:
        filename = meme["filename"]
        exists = "✓" if meme["exists"] else "✗"
        metadata = meme.get("metadata", {})
        emotions = ", ".join(metadata.get("emotions", [])[:3])
        energy = metadata.get("energy", "N/A")

        table.add_row(filename, exists, emotions, energy)

    console.print(table)
    console.print()


def main():
    """Main entry point"""
    app()


if __name__ == "__main__":
    main()
