# -*- mode: python -*-

block_cipher = None


a = Analysis(['checker.py'],
             pathex=['/Users/peter.kos/Code/Python/Music test'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='checker',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
