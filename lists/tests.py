from django.test import TestCase

from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_homepage_content(self):
        response = self.client.get("/")
        self.assertContains(response, "To-Do")

    def test_renders_input_form(self):
        response = self.client.get("/")
        self.assertContains(response, '<form action="/lists/new" method="POST">')
        self.assertContains(response, '<input id="id_new_item" name="item_text"')


class ListItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        my_list = List()
        my_list.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = my_list
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = my_list
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, my_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, my_list)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, my_list)


class ListViewTest(TestCase):
    def test_renders_input_form(self):
        response = self.client.get("/lists/only-one-list/")
        self.assertContains(response, '<form action="/lists/new" method="POST">')
        self.assertContains(response, '<input id="id_new_item" name="item_text"')

    def test_displays_all_list_items(self):
        mylist = List.objects.create()
        Item.objects.create(text="itemey 1", list=mylist)
        Item.objects.create(text="itemey 2", list=mylist)

        response = self.client.get("/lists/only-one-list/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

    def test_uses_list_template(self):
        response = self.client.get("/lists/only-one-list/")
        self.assertTemplateUsed(response, "list.html")


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/only-one-list/")
