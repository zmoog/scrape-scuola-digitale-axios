from axios import GradeParser

def test_parse_grades():

    html = """
<tr role="row" class="odd">
    <td class=" text-center">02/11/2023</td>
    <td class=" text-center">Scienze</td>
    <td class=" text-center">Scritto</td>
    <td class=" text-center"><span class="label bg-green bg-font-green" data-toggle="tooltip" title=""
            data-original-title="Voto: 7,75 <small>(scritto)</small><br>Valore: 7,75">7,75</span></td>
    <td class=" text-center"></td>
    <td>Verifica scritta sull'organizzazione e il rivestimento del corpo umano.</td>
    <td class=" text-center">Micela Silvia</td>
    <td class=" text-center"></td>
</tr>    
    """

    parser = GradeParser()
    grades = parser.parse(html)

    assert len(grades) == 1
    assert grades[0].subject == "Scienze"
    assert grades[0].value == 7.75
