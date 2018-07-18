import glob
import os
import unittest as ut

from Music import HashTable as ht
from Music import MusicHashTable as mht
from Music import YT_Bot as yt

TEST_VIDEO = '6cwBLBCehGg'
testSong00 = mht.Data('home', 'gnash')
testSong01 = mht.Data('SWEET', 'BROCKHAMPTON')
testSong02 = mht.Data('Pillow Talk', 'Zayn')
testSong03 = mht.Data('Kiss You', 'One Direction')
testSong04 = mht.Data('Hurricane', 'Halsey')
testSong05 = mht.Data('i hate u, i love u', 'gnash')
testSong06 = mht.Data('Almost Cut My Hair (For Crosby)', 'Milo')
testSong07 = mht.Data('CINEMA 1', 'BROCKHAMPTON')
testSong08 = mht.Data('Black Car', 'Gregory Alan Isakov')
testSong09 = mht.Data('This House', 'Gregory Alan Isakov')
testSong10 = mht.Data('What Makes You Beautiful', 'One Direction')
testSong11 = mht.Data('Tessa Violet', 'Crush', 'SiAuAJBZuGs', 111000, 4300, 1969889)
testSong12 = mht.Data('Robots', 'Flight of the Conchords', 'BNC61-OOPdA', 4100, 59, 559964)
testSong13 = mht.Data('in cold blood', 'alt-j','rP0uuI80wuY',74000,2000,9059467)

# prints error message
def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))

class TestYT_Bot(ut.TestCase):

    def testIsLive(self):
        self.assertTrue(yt.isLive(['live', 'test', 'test', 'test']))
        self.assertTrue(yt.isLive(['test', 'test', 'live', 'test']))
        self.assertTrue(yt.isLive(['test', 'test', 'test', 'live']))
        self.assertFalse(yt.isLive(['test', 'test', 'test', 'test']))

class TestMusicHashTable(ut.TestCase):
    mht.FileName = 'Test.csv'

    def testMode(self):
        self.assertEqual(mht.FileName, 'Test.csv')

    def testReadData(self):
        desiredResult = []
        mht.clear()
        try:
            data = mht.readData()
            self.assertEqual(data, desiredResult, 'Failed to read from file' + mht.FileName)
        except TypeError and ValueError and FileNotFoundError as e:
            error(str(e))
            pass

    def testSaveHeader(self):
        desiredResult = "[\"['ARTIST', 'TITLE', 'URL', 'HASH', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?']\"]"
        try:
            mht.saveHeader(dataList=['ARTIST', 'TITLE', 'URL', 'HASH', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?'])  # Test
            results = str(mht.readData()[0])  # gather results
            self.assertEqual(results, desiredResult)
        except TypeError and ValueError as e:
            error(str(e))
            pass

    def testSaveData(self):
        try:
            desiredResult = "[['Flight of the Conchords,Robots,BNC61-OOPdA,4100,59,559964,False'], ['Crush,Tessa Violet,SiAuAJBZuGs,111000,4300,1969889,False'], ['gnash,home,6cwBLBCehGg,0,0,0,False'], ['alt-j,in cold blood,rP0uuI80wuY,74000,2000,9059467,False']]"
            dataList = ht.HashTable()
            dataList.put(testSong12.Artist, testSong12)
            dataList.put(testSong11.Artist, testSong11)
            dataList.put(testSong00.Artist, testSong00)
            dataList.put(testSong13.Artist, testSong13)
            mht.clear()
            mht.saveData(dataList)
            results = str(mht.readData())  # gather results
            self.assertEqual(results, desiredResult)
        except ValueError and AttributeError as e:
            error(str(e))
            pass

    def testAppendData(self):
        desiredResult = "[['alt-j,in cold blood,rP0uuI80wuY,74000,2000,9059467,False']]"
        try:
            mht.clear()
            mht.appendData(mht.Data("in cold blood", "alt-j", Url="rP0uuI80wuY", likes=74000,
                                    dislikes=2000, views=9059467))
            results = str(mht.readData()[mht.readData().__len__() - 1:])
            self.assertEqual(desiredResult, results)
        except TypeError and ValueError as e:
            error(str(e))
            pass

    def testGetStats(self):
        desiredResult = [0, 0, 0]
        ytPath = 'https://www.youtube.com/watch?v='
        try:
            results = mht.getStats(ytPath + TEST_VIDEO)
            self.assertEqual(results, desiredResult)
        except TypeError as e:
            error(str(e))
            pass

    def testClear(self):
        desiredResult = 0
        try:
            mht.clear()
            results = mht.readData().__len__()
            self.assertEqual(results, desiredResult)
        except ValueError as e:
            error(str(e))
            pass

    def testToCurrent(self):
        desiredResult = ['Music/Current\Test 0-title-6cwBLBCehGg.mp3',
                         'Music/Current\Test 1-title-6cwBLBCehGg.mp3',
                         'Music/Current\Test 2-title-6cwBLBCehGg.mp3',
                         'Music/Current\Test 3-title-6cwBLBCehGg.mp3',
                         'Music/Current\Test 4-title-6cwBLBCehGg.mp3']
        try:
            musicList = glob.glob(mht.TestMusicPath + '*.mp3')  # gather a list of tracks in /Test/
            for track in musicList:
                if str(track.split(' ')[0])[-4:] == "Test":
                    track = track[mht.TestMusicPath.__len__():]
                    mht.toCurrent(track, '-1')

            results = glob.glob(mht.CurrentMusicPath + '*.mp3')  # gather a list of tracks in /Music/Current/
            for track in results:  # return Test*.mp3 to /Test/
                track = track[mht.CurrentMusicPath.__len__():]
                if track.split(' ')[0] == "Test":
                    os.rename(mht.CurrentMusicPath + track, mht.TestMusicPath + track)
            self.assertEqual(results, desiredResult)
        except TypeError and FileNotFoundError and AttributeError and OSError as e:
            error(str(e))
            pass

    def testUpdateCSV(self):
        desiredResult = [["'ARTIST', 'TITLE', 'URL', 'LIKES', 'DISLIKES', 'VIEWS', 'USED?'"],
                         ['Test 0,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 1,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 2,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 3,title,6cwBLBCehGg,0,0,0,False'],
                         ['Test 4,title,6cwBLBCehGg,0,0,0,False']]
        try:
            mht.clear()
            print(mht.music.__str__())
            mht.music.remove('alt-j')
            print(mht.readData())
            mht.updateCSV(-1)
            results = mht.readData()
            print(results)
            self.assertEqual(results, desiredResult)
        except TypeError as e:
            error(str(e))
            pass

class TestHashTable(ut.TestCase):
    def testH1(self):
        desiredResult = 374
        Table = ht.HashTable()
        result = Table.h1(key="test")
        self.assertEqual(result, desiredResult)

    def testH2(self):
        desiredResult = 24
        Table = ht.HashTable()
        result = Table.h2(key="test")
        self.assertEqual(result, desiredResult)

    def testCutOff(self):
        Table = ht.HashTable(10)
        Table.keys = [[] for i in range(0, 9)]
        self.assertEqual(True, Table.cutoff())
        Table.keys = [[] for i in range(0, 3)]
        self.assertEqual(False, Table.cutoff())

    def testDoubleHashing(self):
        Table = ht.HashTable(10)
        Table.put(testSong00.Artist, testSong00)
        Table.put(testSong01.Artist, testSong01)
        self.assertEqual(1, Table.doubleHashed)
        self.assertEqual(2 * Table.h1(testSong01.Artist) + Table.h2(testSong01.Artist) % Table.capacity,
                         Table.doubleHashing(testSong01.Artist)[1])

    def testGet(self):
        Table = ht.HashTable(5)
        Table.put(testSong00.Artist, testSong00)
        Table.put(testSong02.Artist, testSong02)
        Table.put(testSong03.Artist, testSong03)
        Table.put(testSong04.Artist, testSong04)
        Table.put(testSong05.Artist, testSong05)
        self.assertEqual([testSong00, testSong05], Table.get(testSong00.Artist))
        self.assertEqual([testSong00, testSong05], Table.get(testSong05.Artist))
        self.assertEqual([testSong02], Table.get(testSong02.Artist))
        self.assertEqual([testSong03], Table.get(testSong03.Artist))
        self.assertEqual([testSong04], Table.get(testSong04.Artist))

    def testSearch(self):
        Table = ht.HashTable(5)
        Table.put(testSong00.Artist, testSong00)
        Table.put(testSong02.Artist, testSong02)
        expectedLocation1 = Table.h1(testSong00.Artist)
        expectedLocation2 = Table.doubleHashing(testSong02.Artist)[1] + 1
        self.assertEqual(expectedLocation1, Table.search(testSong00.Artist))
        self.assertEqual(expectedLocation2, Table.search(testSong02.Artist))

    def testRehash(self):
        desiredResult1 = 10
        desiredResult2 = 37
        desiredResult3 = [testSong01.Artist, testSong06.Artist, testSong05.Artist]
        desiredResult4 = [testSong01, testSong06, testSong05, testSong07]
        desiredResult5 = 4
        desiredResult6 = 1
        Table = ht.HashTable(5)
        Table.put(testSong01.Artist, testSong01)
        Table.put(testSong06.Artist, testSong06)
        Table.put(testSong05.Artist, testSong05)
        Table.put(testSong07.Artist, testSong07)

        Table.rehash()
        self.assertEqual(desiredResult6, Table.rehashed)

        self.assertEqual(desiredResult1, Table.capacity)
        Table.keys.sort()
        self.assertEqual(desiredResult3, Table.keys)
        self.assertEqual(desiredResult4, Table.values)
        self.assertEqual(desiredResult5, Table.size)

    def testPut(self):
        Table = ht.HashTable(5)
        Table.put(testSong08.Artist, testSong08)
        Table.put(testSong09.Artist, testSong09)
        self.assertEqual(2, Table.size)
        self.assertEqual([testSong08.Artist], Table.keys)
        self.assertEqual([testSong08, testSong09], Table.values)

    def testRemove(self):
        Table = ht.HashTable(10)
        Table.put(testSong10.Artist, testSong10)
        desiredResult1 = 1
        desiredResult2 = 0
        desiredResult3 = []
        desiredResult4 = [testSong10]
        desiredResult5 = [[], [], [], [], [], [], [], [], [], []]
        desiredResult6 = [testSong10.Artist]
        self.assertEqual(desiredResult1, Table.size)
        self.assertEqual(desiredResult4, Table.values)
        self.assertEqual(desiredResult6, Table.keys)
        Table.remove('One Direction')
        self.assertEqual(desiredResult2, Table.size)
        self.assertEqual(desiredResult3, Table.keys)
        self.assertEqual(desiredResult3, Table.values)
        self.assertEqual(desiredResult5, Table.table)

    def testHas(self):
        Table = ht.HashTable(5)
        Table.put(testSong00.Artist, testSong00)
        self.assertTrue(Table.has(testSong00.Artist))
        self.assertFalse(Table.has(testSong01.Artist))

if __name__ == '__main__':
    ut.main()
