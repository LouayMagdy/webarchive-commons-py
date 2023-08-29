import sys
import logging


class ResourceExtractor:
    _logger = logging.getLogger(__name__)
    TOOL_NAME = "extractor"
    TOOL_DESCRIPTION = "A tool for extracting metadata from WARC, ARC, and WAT files"

    def _usage(self, exit_code):
        """
        this method indicates how to use the overall program
            :param exit_code: an integer passed to the function if the program is mis-used
            :return: exit_code
        """
        print("Usage: ")
        print("extractor [OPT] SRC")
        print("\tSRC is the local path, HTTP or HDFS URL to an arc, warc, arc.gz, or warc.gz.")
        print("\tOPT can be one of:")
        print("\t\t-cdxURL\tProduce output in old URL Wayback CDX format")
        print("\t\t-cdx\tProduce output in NEW-SURT-Wayback CDX format")
        print("\t\t\t (note that column 1 is NOT standard Wayback canonicalized)\n")
        print("\t\t-wat\tembed JSON output in a compressed WARC wrapper, for storage, or sharing.")
        return exit_code

    def run(self, args):
        """
        the main logic of the program is here
        it may raise IndexOutOfBoundsException, FileNotFoundException, IOException, ResourceParseException, URISyntaxException
            :param args: Command line arguments passed to the program
            :return:
        """
        if len(args) < 1 or len(args) > 4:
            return self._usage(1)
        max, arg = sys.maxint, 0
        self._logger.setLevel(logging.WARNING)
        if args[0] == "-strict":




