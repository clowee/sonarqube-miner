from collections import OrderedDict
import pandas as pd
from pathlib import Path
from sonar_object import SonarObject
from utils import process_datetime

SONAR_ANALYSES_TYPE = OrderedDict({
        "project": "object",
        "analysis_key": "object",
        "date": "object",
        "project_version": "object",
        "revision": "object"
})

class Analysis(SonarObject):

    def __init__(self, server, output_path, project_key):
        SonarObject.__init__(
            self,
            endpoint = server + "api/project_analyses/search",
            params =    {
                'p': 1,     # page/iteration
                'ps': 100,  # pageSize
                'project': project_key
            },
            output_path = output_path
        )
        self.__project_key = project_key

    def _write_csv(self):
        analysis_list = []
        for analysis in self._element_list:

            analysis_key = None if 'key' not in analysis else analysis['key']
            date = None if 'date' not in analysis else process_datetime(analysis['date'])
            project_version = None if 'projectVersion' not in analysis else analysis['projectVersion']
            revision = None if 'revision' not in analysis else analysis['revision']
            line = (self.__project_key, analysis_key, date, project_version, revision)
            analysis_list.append(line)

        if analysis_list:

            output_path = Path(self._output_path).joinpath("analysis")
            output_path.mkdir(parents=True, exist_ok=True)

            file_name = self.__project_key.replace(' ', '_').replace(':', '_')
            file_path = output_path.joinpath(f"{file_name}.csv")

            df = pd.DataFrame(data=analysis_list, columns=list(SONAR_ANALYSES_TYPE.keys()))
            df.to_csv(file_path, index=False, header=True)
            return df
        return None

    def get_analyses(self):
        self._query_server(key = 'analyses')
        result = self._write_csv()
        return result
