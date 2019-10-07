
import main
import pytest


def test_file_backup(tmp_path):
    test_files = [(tmp_path / f"{i}.txt") for i in range(4)]
    [f.touch() for f in test_files]
    with main.file_backups(tmp_path, "*.txt") as backups:
        print(backups)
        txt_files = list(tmp_path.rglob("*.txt"))
        txt_backups = list(tmp_path.rglob("*.txt.back"))
        assert len(txt_files) == 0
        assert len(txt_backups) == len(test_files)
        # Should restore missing files
        test_files[0].touch()  # Simulate success
        test_files[1].touch()
        # Should not restore existing files
        test_files[2].write_text("test")
    assert test_files[3].exists()
    assert test_files[2].read_text() == "test"
