from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, SelectField, SubmitField, FileField, FloatField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


class RegistroForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    confirmar = PasswordField("Confirmar Senha", validators=[EqualTo("senha")])
    submit = SubmitField("Registrar")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class ProdutoForm(FlaskForm):
    nome = StringField("Nome do Produto",
                       validators=[DataRequired(), Length(min=3, max=100)])

    descricao = TextAreaField("Descrição")

    preco = DecimalField("Preço",
                         validators=[DataRequired(), NumberRange(min=0)])

    categoria = SelectField("Categoria",
                            choices=[
                                ('Lanche', 'Lanche'),
                                ('Bebida', 'Bebida'),
                                ('Sobremesa', 'Sobremesa'),
                                ('Porção', 'Porção')
                            ],
                            validators=[DataRequired()])

    imagem = FileField('Imagem do Produto (opcional)', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens!')
    ])

    ingredientes = SelectMultipleField('Ingredientes da Receita (segure Ctrl para selecionar vários)', coerce=int)

    submit = SubmitField("Salvar Produto")

    class ProdutoForm(FlaskForm):
        nome = StringField("Nome do Produto",
                           validators=[DataRequired(), Length(min=3, max=100)])

        descricao = TextAreaField("Descrição")

        preco = DecimalField("Preço",
                             validators=[DataRequired(), NumberRange(min=0)])

        categoria = SelectField("Categoria",
                                choices=[
                                    ('Lanche', 'Lanche'),
                                    ('Bebida', 'Bebida'),
                                    ('Sobremesa', 'Sobremesa'),
                                    ('Porção', 'Porção')
                                ],
                                validators=[DataRequired()])

        imagem = FileField('Imagem do Produto (opcional)', validators=[
            FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens!')
        ])

        submit = SubmitField("Salvar Produto")

class IngredienteForm(FlaskForm):
    nome = StringField("Nome do Igrediente",
                       validators=[DataRequired(), Length(min=3, max=100)])

    estoque_atual = FloatField("Quantidade em Estoque",
                               validators=[DataRequired(), NumberRange(min=0)])

    unidade_medida = StringField("Unidade de Medida (ex: g, kg, un, l)",
                                 validators=[DataRequired(), Length(max=20)])

    submit = SubmitField("Salvar Igrediente")