import argparse
from sonar_project import Projects
from sonar_metric import Metrics
from sonar_analysis import Analysis
from sonar_measure import Measures
from sonar_issue import Issues

COURSE_SERVER = "https://course-sonar.rd.tuni.fi/"
SONAR63 = "http://sonar63.rd.tut.fi/"
server = SONAR63

ORGANIZATION = "default-organization"

def fetch_sonar_data(output_path):
    metrics = Metrics(server, output_path)
    metrics_list = metrics.get_metrics()

    prj = Projects(server, ORGANIZATION, output_path)
    projects = prj.get_projects()
    projects.sort(key=lambda x: x['key'])

    print("Total: {0} projects.".format(len(projects)))
    for project in projects:
        print('{0} analysis starts'.format(project['name']))
        analysis = Analysis(server, output_path, project['key'])
        new_analysis = analysis.get_analysis()
        print('{0} analysis completed'.format(project['name']))

        if new_analysis is None:
            continue
        print('{0} measure starts'.format(project['name']))
        measure = Measures(server, project_key=project['key'], output_path=output_path,
                           analyses=new_analysis, measures_type=metrics_list)
        measure.get_measures()
        print('{0} measure completed'.format(project['name']))

        print('{0} issues starts'.format(project['name']))
        issues = Issues(server, output_path, project['key'], analyses=new_analysis)
        issues.get_issues()
        print('{0} issues completed'.format(project['name']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output-path", default='./sonar_data', help="Path to output file directory.")
    args = vars(ap.parse_args())
    output_path = args['output_path']
    fetch_sonar_data(output_path)


if __name__ == '__main__':
    main()
