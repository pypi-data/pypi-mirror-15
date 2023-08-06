import unittest
import re
from deepthought.modules.store.DTQueryBuilder import DTQueryBuilder

class DTQueryBuilderTest(unittest.TestCase):
    def testSelectStatement(self):
        qb = DTQueryBuilder(None)
        qb.fromT("test_table t1")
        qb.join("another_table t2","t1.id=t2.t1_id")
        qb.leftJoin("third_table t3","t2.id=t3.t2_id")
        qb.where("test=success")
        qb.having("1=1")
        qb.groupBy("test_col")
        qb.orderBy("test_col DESC")
        qb.limit(10)
        self.assertEquals("SELECT test_col FROM test_table t1  JOIN another_table t2 ON (t1.id=t2.t1_id) LEFT JOIN third_table t3 ON (t2.id=t3.t2_id) WHERE (test=success) GROUP BY test_col HAVING (1=1) ORDER BY test_col DESC LIMIT 10",qb.selectStatement("test_col"))

    def testFormatValue(self):
        qb = DTQueryBuilder(None)
        self.assertEquals("NULL",qb.formatValue(None))
        self.assertEquals('\'{"test": "success"}\'',qb.formatValue({"test": "success"}))
        self.assertEquals('SELECT * FROM test',qb.formatValue("\\DTSQLEXPR\\SELECT * FROM test"))
        self.assertEquals('\'Any old string\'',qb.formatValue("Any old string"))

        qb.filter({"id":"1 OR 1=1"})
        self.assertIsNone(re.search(r"id=1 OR 1=1",qb.selectStatement()))

if __name__ == '__main__':
    unittest.main()
