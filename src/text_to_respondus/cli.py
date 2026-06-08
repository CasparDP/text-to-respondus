"""
Command line interface for text-to-respondus converter.
"""

import click
import logging
from pathlib import Path
from typing import Optional

from .converter import QuizConverter, create_output_directory

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version='0.1.0')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(verbose: bool) -> None:
    """Text to Respondus Converter - Convert quiz files to Respondus CSV format."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)


@main.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.argument('output_file', type=click.Path(path_type=Path))
@click.option('--topic', '-t', default='', help='Topic name for the quiz')
@click.option('--difficulty', '-d', default='', help='Difficulty level')
@click.option('--preview', '-p', is_flag=True, help='Show preview before conversion')
@click.option('--stats', '-s', is_flag=True, help='Show conversion statistics')
def convert(
    input_file: Path, 
    output_file: Path, 
    topic: str, 
    difficulty: str,
    preview: bool,
    stats: bool
) -> None:
    """Convert a quiz text file to Respondus CSV format."""
    
    converter = QuizConverter()
    
    # Validate input file
    if not converter.validate_input_file(str(input_file)):
        click.echo(f"❌ Error: Cannot parse input file {input_file}", err=True)
        raise click.Abort()
    
    # Show statistics if requested
    if stats:
        click.echo("📊 Conversion Statistics:")
        stats_data = converter.get_conversion_stats(str(input_file))
        if "error" in stats_data:
            click.echo(f"❌ Error getting stats: {stats_data['error']}", err=True)
        else:
            for key, value in stats_data.items():
                click.echo(f"   {key.replace('_', ' ').title()}: {value}")
        click.echo()
    
    # Show preview if requested
    if preview:
        click.echo("👀 Preview (first 3 questions):")
        preview_df = converter.preview_conversion(str(input_file), topic, 3)
        if preview_df is not None:
            # Show just the key columns for readability
            preview_cols = ['Question Title/Id', 'Question Wording', 'Correct Answer', 'Choice 1', 'Choice 2']
            available_cols = [col for col in preview_cols if col in preview_df.columns]
            click.echo(preview_df[available_cols].to_string(index=False, max_colwidth=50))
        else:
            click.echo("❌ Could not generate preview", err=True)
        click.echo()
        
        if not click.confirm("Continue with conversion?"):
            click.echo("Conversion cancelled.")
            return
    
    # Create output directory if needed
    create_output_directory(str(output_file))
    
    # Perform conversion
    click.echo(f"🔄 Converting {input_file} to {output_file}...")
    
    success = converter.convert_file(
        str(input_file), 
        str(output_file), 
        topic=topic,
        difficulty=difficulty
    )
    
    if success:
        click.echo(f"✅ Successfully converted to {output_file}")
        
        # Show file size
        if output_file.exists():
            size_kb = output_file.stat().st_size / 1024
            click.echo(f"📄 Output file size: {size_kb:.1f} KB")
    else:
        click.echo("❌ Conversion failed", err=True)
        raise click.Abort()


@main.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument('output_dir', type=click.Path(file_okay=False, path_type=Path))
def batch(input_dir: Path, output_dir: Path) -> None:
    """Convert every .txt quiz file in a folder to Respondus CSV."""

    quiz_files = sorted(input_dir.glob('*.txt'))

    if not quiz_files:
        click.echo(f"❌ No .txt files found in {input_dir}", err=True)
        raise click.Abort()

    output_dir.mkdir(parents=True, exist_ok=True)
    converter = QuizConverter()

    failures = 0
    for quiz_file in quiz_files:
        output_file = output_dir / f"{quiz_file.stem}_respondus.csv"
        click.echo(f"🔄 {quiz_file.name} → {output_file.name}")

        if not converter.convert_file(
            str(quiz_file), str(output_file), topic=quiz_file.stem
        ):
            click.echo(f"❌ Failed: {quiz_file.name}", err=True)
            failures += 1

    converted = len(quiz_files) - failures
    click.echo(f"✅ Converted {converted}/{len(quiz_files)} file(s) to {output_dir}")

    if failures:
        raise click.Abort()


@main.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--topic', '-t', default='', help='Topic name for the quiz')
def validate(input_file: Path, topic: str) -> None:
    """Validate a quiz text file without converting."""
    
    converter = QuizConverter()
    
    click.echo(f"🔍 Validating {input_file}...")
    
    if converter.validate_input_file(str(input_file)):
        click.echo("✅ File is valid and can be converted")
        
        # Show stats
        stats = converter.get_conversion_stats(str(input_file))
        if "error" not in stats:
            click.echo("\n📊 File Statistics:")
            for key, value in stats.items():
                click.echo(f"   {key.replace('_', ' ').title()}: {value}")
    else:
        click.echo("❌ File validation failed", err=True)
        raise click.Abort()


@main.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--topic', '-t', default='', help='Topic name for the quiz')
@click.option('--num-questions', '-n', default=5, help='Number of questions to preview')
def preview(input_file: Path, topic: str, num_questions: int) -> None:
    """Preview how questions will look in Respondus format."""
    
    converter = QuizConverter()
    
    click.echo(f"👀 Previewing {input_file} (first {num_questions} questions)...")
    
    preview_df = converter.preview_conversion(str(input_file), topic, num_questions)
    
    if preview_df is not None:
        # Display key columns
        key_cols = ['Question Title/Id', 'Question Wording', 'Correct Answer', 'Choice 1', 'Choice 2', 'Choice 3']
        available_cols = [col for col in key_cols if col in preview_df.columns]
        
        click.echo(preview_df[available_cols].to_string(index=False, max_colwidth=60))
        
        click.echo(f"\n📝 Preview shows {len(preview_df)} questions")
        click.echo("💡 Use 'convert' command to generate full CSV file")
    else:
        click.echo("❌ Could not generate preview", err=True)
        raise click.Abort()


@main.command()
def info() -> None:
    """Show information about the converter."""
    
    click.echo("🔧 Text to Respondus Converter")
    click.echo("Version: 0.1.0")
    click.echo()
    click.echo("📝 Supported Input Format:")
    click.echo("   - Canvas-style quiz text files")
    click.echo("   - Multiple choice questions")
    click.echo("   - Correct answers marked with *")
    click.echo()
    click.echo("📤 Output Format:")
    click.echo("   - Respondus CSV format")
    click.echo("   - Compatible with ANS and other LMS systems")
    click.echo()
    click.echo("🔗 Example Usage:")
    click.echo("   text-to-respondus convert quiz.txt output.csv --topic 'Week 1'")
    click.echo("   text-to-respondus validate quiz.txt")
    click.echo("   text-to-respondus preview quiz.txt --num-questions 3")


if __name__ == '__main__':
    main()
