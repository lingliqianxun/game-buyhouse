# -*- mode: python -*-
import os,sys

py_name = sys.argv[1].split('.')[0] + ".py"
cur_path = os.getcwd()
ico_name = 'ico.ico'
ico_path = cur_path + "\\" + ico_name
exe_name = 'buyhouse'


block_cipher = None

a = Analysis([py_name],
             pathex=[cur_path],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [(ico_name, ico_path, 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=exe_name,
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )

