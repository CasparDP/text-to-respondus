"""Tests for the command line interface."""

from click.testing import CliRunner

from text_to_respondus.cli import main


SAMPLE_QUIZ = """\
Title: Test Question
Points: 1
1. What is the capital of France?
... Paris is the capital of France.
a) London
*b) Paris
c) Berlin
"""


def test_batch_converts_all_txt_files(tmp_path):
    """`batch` converts every .txt file in a folder to a Respondus CSV."""
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    input_dir.mkdir()
    (input_dir / "quiz_one.txt").write_text(SAMPLE_QUIZ, encoding="utf-8")
    (input_dir / "quiz_two.txt").write_text(SAMPLE_QUIZ, encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(main, ["batch", str(input_dir), str(output_dir)])

    assert result.exit_code == 0, result.output
    assert (output_dir / "quiz_one_respondus.csv").exists()
    assert (output_dir / "quiz_two_respondus.csv").exists()

    content = (output_dir / "quiz_one_respondus.csv").read_text(encoding="utf-8")
    assert "Question Type" in content
    assert "capital of France" in content


def test_batch_errors_when_no_txt_files(tmp_path):
    """`batch` exits non-zero when the input folder has no .txt files."""
    input_dir = tmp_path / "empty"
    input_dir.mkdir()

    runner = CliRunner()
    result = runner.invoke(main, ["batch", str(input_dir), str(tmp_path / "out")])

    assert result.exit_code != 0
